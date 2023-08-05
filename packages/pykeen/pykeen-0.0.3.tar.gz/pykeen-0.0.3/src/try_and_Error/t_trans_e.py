
import torch
import torch.nn as nn
import numpy as np
import torch.optim as optim

class TransE(nn.Module):
    def __init__(self):
        super(TransE, self).__init__()
        self.entities_embs = torch.nn.Embedding(3, 2)
        pre_trained_entities = np.array([[1., 1.], [2., 2.], [40., -500.]])
        self.entities_embs.weight.data.copy_(torch.from_numpy(pre_trained_entities))

        self.relation_embs = torch.nn.Embedding(1, 2)
        pre_trained_relation = np.array([[3., 3.]])
        self.relation_embs.weight.data.copy_(torch.from_numpy(pre_trained_relation))

        print("############## Initialised Embeddigns#############")
        print(self.entities_embs.weight.data)
        print()
        print(self.relation_embs.weight.data)

        self.criterion = nn.MarginRankingLoss(margin=3., size_average=True)

    def compute_score(self, h_embs, r_embs, t_embs):
        """

        :param h_embs:
        :param r_embs:
        :param t_embs:
        :return:
        """

        # Add the vector element wise
        sum_res = h_embs + r_embs - t_embs

        # Square root
        square_res = torch.mul(sum_res, sum_res)
        reduced_sum_res = torch.sum(square_res, 1)

        # Take the square root element wise
        sqrt_res = torch.sqrt(reduced_sum_res)
        # The scores are the negative distane
        distances = sqrt_res

        n = torch.norm(sum_res).view(size=(-1,))
        print("score norm shape: ", n.shape)
        print("distances shape: ", distances.shape)
        print("score norm: ", n)
        print("distances shape: ", distances)
        exit(0)

        return distances

    def compute_loss(self, pos_scores, neg_scores):
        """

        :param pos_scores:
        :param neg_scores:
        :return:
        """

        # y == -1 indicates that second input to criterion should get a larger loss
        # y = torch.Tensor([-1]).cuda()
        # NOTE: y = 1 is important
        y = np.repeat([-1],repeats=pos_scores.shape[0])
        # y = torch.tensor([-1], dtype=torch.float)
        y = torch.tensor(y, dtype=torch.float)

        # Scores for the psotive and negative triples
        pos_scores = torch.tensor(pos_scores, dtype=torch.float)
        neg_scores = torch.tensor(neg_scores, dtype=torch.float)

        loss = self.criterion(pos_scores, neg_scores, y)

        return loss


if __name__ == '__main__':

    trans_e = TransE()
    print('##################################################')

    print()
    print('###########Compute Score###########')
    pos_heads = torch.tensor([[2]],dtype=torch.long)
    pos_tails = torch.tensor([[0]], dtype=torch.long)
    rels = torch.tensor([[0]], dtype=torch.long)

    neg_heads = torch.tensor([[2]], dtype=torch.long)
    neg_tails = torch.tensor([[2]], dtype=torch.long)

    pos_h_embs = trans_e.entities_embs(pos_heads).view(-1,2)
    pos_t_embs = trans_e.entities_embs(pos_tails).view(-1,2)
    neg_h_embs = trans_e.entities_embs(neg_heads).view(-1, 2)
    neg_t_embs = trans_e.entities_embs(neg_tails).view(-1, 2)
    rel_embs = trans_e.relation_embs(rels).view(-1,2)

    pos_score = trans_e.compute_score(pos_h_embs, rel_embs, pos_t_embs)
    neg_score = 1 * trans_e.compute_score(neg_h_embs, rel_embs, neg_t_embs)

    print("pos_score: ", pos_score)
    print("neg_score: ", neg_score)

    print("###########Apply SGD#########")
    optimizer = optim.SGD(trans_e.parameters(), lr=0.1)

    optimizer.zero_grad()

    loss = trans_e.compute_loss(pos_score,neg_score)
    # loss = loss.copy(1.000590)
    # loss = torch.tensor([1.000590],dtype=torch.float)

    print("loss: ", loss)

    loss.backward()


    for p in trans_e.parameters():
        if p.requires_grad:
            print(p.grad)



