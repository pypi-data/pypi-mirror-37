import requests
import base64

class Connection:
    def __init__(self, auth_key, server='api.basilica.ai'):
        self.server = server
        self.session = requests.Session()
        self.session.auth = (auth_key, '')

    def __enter__(self, *a, **kw):
        self.session.__enter__(*a, **kw)
        return self

    def __exit__(self, *a, **kw):
        return self.session.__exit__(*a, **kw)

    def raw_embed(self, url, data, opts={}):
        if type(url) != str:
            raise ValueError('`url` argument must be a string (got `%s`)' % url)
        if type(opts) != dict:
            raise ValueError('`url` argument must be a dict (got `%s`)' % url)
        if 'data' in opts:
            raise ValueError('`opts` argument may not contain `data` key (got `%s`)' % opts)
        query = opts.copy()
        query['data'] = data
        res = self.session.post(url, json=query)
        out = res.json()
        if 'error' in out:
            raise RuntimeError('basilica.ai server returned error: `%s`' % out['error'])
        if 'embeddings' not in out:
            raise RuntimeError('basilica.ai server did not return embeddings: `%s`' % out)
        return out['embeddings']

    # TODO: parallelize
    def embed(self, url, data, batch_size=64, **kw):
        batch = []
        for i in data:
            batch.append(i)
            if len(batch) >= batch_size:
                for e in self.raw_embed(url, batch, **kw):
                    yield e
                batch = []
        if len(batch) > 0:
            for e in self.raw_embed(url, batch, **kw):
                yield e
            batch = []

    def embed_images(self, images, model='generic', version='default', https=True, **kw):
        url = '%s://%s/embed/images/%s/%s' % (
            'https' if https else 'http', self.server, model, version)
        data = ({'img': base64.b64encode(img).decode('utf-8')} for img in images)
        return self.embed(url, data, **kw)

    def embed_image(self, image, *a, **kw):
        return list(self.embed_images([image], *a, **kw))[0]

    def embed_image_files(self, image_files, *a, **kw):
        def load_image_files(image_files):
            for image_file in image_files:
                with open(image_file, 'rb') as f:
                    yield f.read()
        return self.embed_images(load_image_files(image_files), *a, **kw)

    def embed_image_file(self, image_file, *a, **kw):
        with open(image_file, 'rb') as f:
            return self.embed_image(f.read(), *a, **kw)

    def embed_sentences(self, sentences, model='english', version='default', https=True, **kw):
        url = '%s://api.basilica.ai/embed/text/%s/%s' % (
            'https' if https else 'http', model, version)
        data = sentences
        return self.embed(url, data, **kw)

    def embed_sentence(self, sentence, *a, **kw):
        return list(self.embed_sentences([sentence], *a, **kw))[0]
