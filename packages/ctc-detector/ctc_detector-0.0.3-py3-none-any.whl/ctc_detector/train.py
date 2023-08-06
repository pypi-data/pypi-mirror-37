# python built-in library
import os
import argparse
import time
from multiprocessing import Manager
# 3rd party library
import numpy as np
import torch
import torch.nn as nn
from torch.nn.utils import clip_grad_norm
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
# own code
from config import config
from model import build_model
from dataset import CTCDataset, Compose
from helper import AverageMeter, iou_mean, prob_to_segment, save_ckpt, load_ckpt
from loss import focal_criterion

def main(resume=True, n_epoch=None, learn_rate=None):
    model_name = config['param']['model']
    if learn_rate is None:
        learn_rate = config['param'].getfloat('learn_rate')
    width = config.getint(model_name, 'width')
    # weight_map = config['param'].getboolean('weight_map')
    c = config['train']
    log_name = c.get('log_name')
    n_batch = c.getint('n_batch')
    n_worker = c.getint('n_worker')
    n_cv_epoch = c.getint('n_cv_epoch')
    if n_epoch is None:
        n_epoch = c.getint('n_epoch')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = build_model(model_name)
    model = model.to(device)

    # define optimizer
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.learn_rate,
        weight_decay=1e-6
        )

    # dataloader workers are forked process thus we need a IPC manager to keep cache in same memory space
    manager = Manager()
    cache = manager.dict()
    compose = Compose()
    # prepare dataset, split train dataset as CV, aka. train-valid
    train_dataset = CTCDataset('data/train', transform=compose, cache=cache)
    train_dataset, train_valid_dataset = train_dataset.split()
    test_valid_dataset = CTCDataset('data/valid', policy='Once', transform=compose, cache=cache)
    # data loader
    def loader(ds):
        return DataLoader(
            ds,
            sampler=ds.sampler(),
            batch_size=n_batch,
            num_workers=n_worker,
            pin_memory=torch.cuda.is_available())
    train_loader = loader(train_dataset)
    train_valid_loader = loader(train_valid_dataset)
    test_valid_loader = loader(test_valid_dataset)

    # resume checkpoint
    start_epoch = iou_tr = iou_cv = 0
    if resume:
        start_epoch = load_ckpt(model, optimizer)
    if start_epoch == 0:
        print('Grand new training ...')

    # put model to GPU
    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = nn.DataParallel(model)

    # decide log directory name
    log_dir = os.path.join(
        'logs', log_name, '{}-{}'.format(model_name, width),
        'ep_{},{}-lr_{}'.format(
            start_epoch,
            n_epoch + start_epoch,
            learn_rate,
        )
    )

    with SummaryWriter(log_dir) as writer:
        if start_epoch == 0 and False:
            # dump graph only for very first training, disable by default
            dump_graph(model, writer, n_batch, width)
        print('Training started ...')
        for epoch in range(start_epoch + 1, n_epoch + start_epoch + 1): # 1 base
            iou_tr = train(train_loader, model, optimizer, epoch, writer)
            if epoch % n_cv_epoch == 0:
                with torch.no_grad():
                    iou_cv = valid(train_valid_loader, model, epoch, writer, 'train')
                    _      = valid(test_valid_loader , model, epoch, writer, 'valid')
            save_ckpt(model, optimizer, epoch, iou_tr, iou_cv)
        print('Training finished ...')

def dump_graph(model, writer, n_batch, width):
    # Prerequisite
    # $ sudo apt-get install libprotobuf-dev protobuf-compiler
    # $ pip3 install onnx
    print('Dump model graph ...')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dummy_input = torch.rand(n_batch, 3, width, width, device=device)
    torch.onnx.export(model, dummy_input, "checkpoint/model.pb", verbose=False)
    writer.add_graph_onnx("checkpoint/model.pb")

def train(loader, model, optimizer, epoch, writer):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    iou = AverageMeter()   # semantic IoU
    print_freq = config['train'].getfloat('print_freq')
    model_name = config['param']['model']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Sets the module in training mode.
    model.train()
    end = time.time()
    n_step = len(loader)
    for i, data in enumerate(loader):
        # measure data loading time
        data_time.update(time.time() - end)
        # split sample data
        inputs = data['image'].to(device)
        labels = data['label'].to(device)
        # zero the parameter gradients
        optimizer.zero_grad()
        # forward step
        outputs = model(inputs)
        # compute loss
        # weight_criterion equals to segment_criterion if weights is none
        loss = focal_criterion(outputs, labels, weights=None)
        # compute gradient and do backward step
        loss.backward()
        # clip_grad_norm(model.parameters(), 2.0) # handle gradient explosion when needed
        optimizer.step()
        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()
        # measure accuracy and record loss
        losses.update(loss.item(), inputs.size(0))
        outputs = prob_to_segment(outputs)
        batch_iou = iou_mean(outputs, labels)
        iou.update(batch_iou, inputs.size(0))
        # log to summary
        if (i + 1) % print_freq == 0:
            print(
                'Epoch: [{0}][{1}/{2}]\t'
                'Time: {batch_time.avg:.2f} (io: {data_time.avg:.2f})\t'
                'Loss: {loss.avg:.4f}\t'
                'IoU: {iou.avg:.3f}\t'
                .format(
                    epoch, i+1, n_step, batch_time=batch_time,
                    data_time=data_time, loss=losses, iou=iou
                )
            )
    # end of loop, dump epoch summary
    writer.add_scalar('training/epoch_loss', losses.avg, epoch)
    writer.add_scalar('training/epoch_iou', iou.avg, epoch)
    return iou.avg # return epoch average iou

def valid(loader, model, epoch, writer, name):
    iou = AverageMeter()   # semantic IoU
    losses = AverageMeter()
    model_name = config['param']['model']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Sets the model in evaluation mode.
    model.eval()
    for i, data in enumerate(loader):
        # get the inputs
        inputs = data['image'].to(device)
        labels = data['label'].to(device)
        # forward step
        outputs = model(inputs)
        # compute loss
        loss = focal_criterion(outputs, labels, weights=None)
        # measure accuracy and record loss (Non-instance level IoU)
        losses.update(loss.item(), inputs.size(0))
        batch_iou = iou_mean(outputs, labels)
        iou.update(batch_iou, inputs.size(0))
    # end of loop, dump epoch summary
    writer.add_scalar('CV_{}/epoch_loss'.format(name), losses.avg, epoch)
    writer.add_scalar('CV_{}/epoch_iou'.format(name), iou.avg, epoch)
    print(
        'Epoch: [{0}]\t\tCV: {1}\t\t'
        'Loss: {loss.avg:.4f}\t'
        'IoU: {iou.avg:.3f}\t'
        .format(epoch, name, loss=losses, iou=iou)
    )
    return iou.avg # return epoch average iou

if __name__ == '__main__':
    learn_rate = config['param'].getfloat('learn_rate')
    n_epoch = config['train'].getint('n_epoch')
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', dest='resume', action='store_true')
    parser.add_argument('--no-resume', dest='resume', action='store_false')
    parser.add_argument('--epoch', type=int, help='run number of epoch')
    parser.add_argument('--lr', type=float, dest='learn_rate', help='learning rate')
    parser.set_defaults(resume=True, epoch=n_epoch, learn_rate=learn_rate)
    args = parser.parse_args()

    main(args.resume, args.epoch, args.learn_rate)