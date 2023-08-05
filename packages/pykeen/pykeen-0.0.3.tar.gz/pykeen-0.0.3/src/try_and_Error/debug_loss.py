
import torch
import torch.autograd
import torch.nn as nn

if __name__ == '__main__':
    pos_scores = torch.tensor([-7.9980, -7.0185, -8.3990], dtype=torch.float)
    neg_scores = torch.tensor([-7.9980, -7.9268, -6.7853], dtype=torch.float)


    criterion = nn.MarginRankingLoss(margin=1, size_average=True)
    y = torch.tensor([1,1,1], dtype=torch.float)
    loss = criterion(pos_scores, neg_scores, y)

    print(loss)