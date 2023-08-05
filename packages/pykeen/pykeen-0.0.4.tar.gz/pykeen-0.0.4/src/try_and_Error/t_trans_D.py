
import torch
import torch.nn.functional as F
import torch.nn as nn
import numpy as np
import torch.optim as optim

class TransD(nn.Module):

    def __init__(self):
        super(TransD, self).__init__()
        self.num_entities = 2
        self.num_relations = 2
        self.entity_embedding_dim = 2
        self.relation_embedding_dim = 3
        self.margin_loss = 1
  

        # A simple lookup table that stores embeddings of a fixed dictionary and size
        self.entity_embeddings = nn.Embedding(self.num_entities, self.entity_embedding_dim, max_norm=1)
        self.relation_embeddings = nn.Embedding(self.num_relations, self.relation_embedding_dim, max_norm=1)
        self.entity_projections = nn.Embedding(self.num_entities, self.entity_embedding_dim)
        self.relation_projections = nn.Embedding(self.num_relations, self.relation_embedding_dim)

        self.criterion = nn.MarginRankingLoss(margin=self.margin_loss, size_average=True)
        self.scoring_fct_norm = 1
        # self._initialize()

    def _compute_scores(self, h_embs, r_embs, t_embs):
        """

        :param h_embs:
        :param r_embs:
        :param t_embs:
        :return:
        """

        # Add the vector element wise
        sum_res = h_embs + r_embs - t_embs
        distances = torch.norm(sum_res, dim=1, p=self.scoring_fct_norm).view(size=(-1,))
        distances = torch.mul(distances, distances)

        return distances

    def _compute_loss(self, pos_scores, neg_scores):
        """

        :param pos_scores:
        :param neg_scores:
        :return:
        """

        # y == -1 indicates that second input to criterion should get a larger loss
        # y = torch.Tensor([-1]).cuda()
        # NOTE: y = 1 is important
        # y = torch.tensor([-1], dtype=torch.float)
        y = np.repeat([-1], repeats=pos_scores.shape[0])
        y = torch.tensor(y, dtype=torch.float)

        # Scores for the psotive and negative triples
        pos_scores = torch.tensor(pos_scores, dtype=torch.float)
        neg_scores = torch.tensor(neg_scores, dtype=torch.float)

        loss = self.criterion(pos_scores, neg_scores, y)

        return loss

    def _project_entities(self, entity_embs, entity_proj_vecs, relation_projs):
        # batch_size = entity_embs.shape[0]
        # identity_matrices = torch.eye(batch_size,self.relation_embedding_dim,self.entity_embedding_dim)
        entity_embs = entity_embs
        relation_projs = relation_projs.unsqueeze(-1)
        entity_proj_vecs = entity_proj_vecs.unsqueeze(-1).permute([0,2,1])

        transfer_matrices = torch.matmul(relation_projs,entity_proj_vecs)



        # transfer_matrices = torch.einsum('nm1,nk1->nmk',
        #                                  [relation_projs, entity_proj_vecs])  # TODO: Check + identity_matrices


        # a = relation_projs.view(-1,self.relation_embedding_dim)
        # torch.matmul(transfer_matrices)

        projected_entity_embs = torch.einsum('nmk,nk->nm', [transfer_matrices, entity_embs])
        # projected_entity_embs = F.normalize(projected_entity_embs, 2, 1)

        return projected_entity_embs

    # def _initialize(self):
    #     lower_bound = -6 / np.sqrt(self.entity_embedding_dim)
    #     upper_bound = 6 / np.sqrt(self.entity_embedding_dim)
    #     nn.init.uniform_(self.entity_embeddings.weight.data, a=lower_bound, b=upper_bound)
    #     nn.init.uniform_(self.relation_embeddings.weight.data, a=lower_bound, b=upper_bound)
    #
    #     norms = torch.norm(self.relation_embeddings.weight, p=2, dim=1).data
    #     self.relation_embeddings.weight.data = self.relation_embeddings.weight.data.div(
    #         norms.view(self.num_relations, 1).expand_as(self.relation_embeddings.weight))

    def forward(self, batch_positives, batch_negatives):
        pos_heads = batch_positives[:, 0:1]
        pos_relations = batch_positives[:, 1:2]
        pos_tails = batch_positives[:, 2:3]

        neg_heads = batch_negatives[:, 0:1]
        neg_relations = batch_negatives[:, 1:2]
        neg_tails = batch_negatives[:, 2:3]

        pos_h_embs = self.entity_embeddings(pos_heads).view(-1, self.entity_embedding_dim)
        pos_r_embs = self.relation_embeddings(pos_relations).view(-1, self.relation_embedding_dim)
        pos_t_embs = self.entity_embeddings(pos_tails).view(-1, self.entity_embedding_dim)

        pos_h_proj_vec_embs = self.entity_projections(pos_heads).view(-1, self.entity_embedding_dim)
        pos_r_projs_embs = self.relation_projections(pos_relations).view(-1, self.relation_embedding_dim)
        pos_t_proj_vec_embs = self.entity_projections(pos_tails).view(-1, self.entity_embedding_dim)

        neg_h_embs = self.entity_embeddings(neg_heads).view(-1, self.entity_embedding_dim)
        neg_r_embs = self.relation_embeddings(neg_relations).view(-1, self.relation_embedding_dim)
        neg_t_embs = self.entity_embeddings(neg_tails).view(-1, self.entity_embedding_dim)

        neg_h_proj_vec_embs = self.entity_projections(neg_heads).view(-1, self.entity_embedding_dim)
        neg_r_projs_embs = self.relation_projections(neg_relations).view(-1, self.relation_embedding_dim)
        neg_t_proj_vec_embs = self.entity_projections(neg_tails).view(-1, self.entity_embedding_dim)

        # Project entities
        proj_pos_heads = self._project_entities(pos_h_embs, pos_h_proj_vec_embs, pos_r_projs_embs)
        proj_pos_tails = self._project_entities(pos_t_embs, pos_t_proj_vec_embs, pos_r_projs_embs)

        proj_neg_heads = self._project_entities(neg_h_embs, neg_h_proj_vec_embs, neg_r_projs_embs)
        proj_neg_tails = self._project_entities(neg_t_embs, neg_t_proj_vec_embs, neg_r_projs_embs)

        pos_scores = self._compute_scores(h_embs=proj_pos_heads, r_embs=pos_r_embs, t_embs=proj_pos_tails)
        neg_scores = self._compute_scores(h_embs=proj_neg_heads, r_embs=neg_r_embs, t_embs=proj_neg_tails)

        # pos_scores = self._compute_scores(h_embs=pos_h_embs, r_embs=pos_r_embs, t_embs=pos_t_embs)
        # neg_scores = self._compute_scores(h_embs=neg_h_embs, r_embs=neg_r_embs, t_embs=neg_t_embs)


        loss = self._compute_loss(pos_scores=pos_scores, neg_scores=neg_scores)

        return loss
    
if __name__ == '__main__':
    pos_heads = torch.tensor([0, 1])
    pos_rels = torch.tensor([0, 0])
    pos_tails = torch.tensor([0, 0])


    # criterion = nn.MarginRankingLoss(margin=1, size_average=True)

    num_entities = 2
    num_relations = 2
    relation_embedding_dim = 3
    entity_embedding_dim = 2
    batch_size = 2

    pos_heads = torch.tensor([0, 1])
    pos_rels = torch.tensor([0, 0])
    pos_tails = torch.tensor([0, 0])

    neg_heads = torch.tensor([1, 0])
    neg_rels = torch.tensor([1, 1])
    neg_tails = torch.tensor([1, 0])

    pos_batch = torch.tensor([[0,0,0],[1,0,0]],dtype=torch.long)
    neg_batch = torch.tensor([[1,1,1], [0,1,0]], dtype=torch.long)

    entity_embeddings = nn.Embedding(num_entities, entity_embedding_dim,max_norm=1)
    relation_embeddings = nn.Embedding(num_relations, relation_embedding_dim,max_norm=1)
    entity_projections = nn.Embedding(num_entities, entity_embedding_dim)
    relation_projections = nn.Embedding(num_relations, relation_embedding_dim)
    model = TransD()
    optimizer = optim.SGD(model.parameters(), lr=0.1)
    for i in range(5):
        loss = model(pos_batch,neg_batch)
        loss.backward()
        print(loss)

        optimizer.step()
        optimizer.zero_grad()
        
        # pos_h_embs = entity_embeddings(pos_heads).view(-1, entity_embedding_dim)
        # pos_r_embs = relation_embeddings(pos_rels).view(-1, relation_embedding_dim)
        # pos_t_embs = entity_embeddings(pos_tails).view(-1, entity_embedding_dim)
        #
        # pos_h_projs_embs = entity_projections(pos_heads).view(-1, entity_embedding_dim)
        # pos_r_projs_embs = relation_projections(pos_rels).view(-1, relation_embedding_dim)
        # pos_t_projs_embs = entity_projections(pos_tails).view(-1, entity_embedding_dim)
        #
        # neg_h_embs = entity_embeddings(pos_heads).view(-1, entity_embedding_dim)
        # neg_r_embs = relation_embeddings(pos_rels).view(-1, relation_embedding_dim)
        # neg_t_embs = entity_embeddings(pos_tails).view(-1, entity_embedding_dim)
        #
        # neg_h_projs_embs = entity_projections(neg_heads).view(-1, entity_embedding_dim)
        # neg_r_projs_embs = relation_projections(neg_rels).view(-1, relation_embedding_dim)
        # neg_t_projs_embs = entity_projections(neg_tails).view(-1, entity_embedding_dim)
        #
        # pos_transfer_matrices = torch.einsum('nm,nk->nmk', [pos_r_projs_embs, pos_h_projs_embs])
        # pos_projected_entity_embs = torch.einsum('nmk,nk->nm', [pos_transfer_matrices, pos_h_embs])
        #
        # pos_sum_res = pos_projected_entity_embs + pos_r_embs - pos_projected_entity_embs
        # pos_distances = torch.norm(pos_sum_res, dim=1, p=1).view(size=(-1,))
        # pos_distances = torch.mul(pos_distances, pos_distances)
        #
        # neg_transfer_matrices = torch.einsum('nm,nk->nmk', [neg_r_projs_embs, neg_h_projs_embs])
        # neg_projected_entity_embs = torch.einsum('nmk,nk->nm', [neg_transfer_matrices, neg_h_embs])
        #
        # neg_sum_res = neg_projected_entity_embs + neg_r_embs - neg_projected_entity_embs
        # neg_distances = torch.norm(neg_sum_res, dim=1, p=1).view(size=(-1,))
        # neg_distances = torch.mul(neg_distances, neg_distances)
        #
        #
        # y = np.repeat([-1], repeats=2)
        # y = torch.tensor(y, dtype=torch.float)
        #
        # # Scores for the psotive and negative triples
        # pos_scores = torch.tensor(pos_distances, dtype=torch.float)
        #
        # loss = criterion(pos_scores, neg_distances, y)
        #
        # print(loss)
        #
        # loss.backward()
        #


