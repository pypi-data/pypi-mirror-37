import json
if __name__ == '__main__':
    path = '/Users/mehdi/.kg_embeddings_pipeline/csqa_wiki_data/temp.json'
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    subjects = data.keys()
    predicates = data.values()
    print(subjects)
    print()
    print(predicates)
    print()

    for p in predicates:
        print(p)
        print()

    print(len(subjects))
    print(len(predicates))