
import os
import getpass


if __name__ == '__main__':
    base_dir = os.environ.get('KG',os.path.join('/data', getpass.getuser(), 'kg_embeddings_pipeline'))
    os.makedirs(base_dir, exist_ok=True)

    print(base_dir)
    print(getpass.getuser())
