from flask import Flask
import couchdb

couch = couchdb.Server('http://admin:YOURPASSWORD@couchserver:5984/')
db = couch['manifest'] #select the database
app = Flask(__name__)

iiif_url = 'https://localhost:3000/iiif/'

@app.route('/')
def index():
    return '<p>Hello, World!</p>'

@app.route('/iiif/collection/<collection_id>')
def collection(collection_id):
    return '<p>Hello, Collection!</p>'


@app.route('/iiif/manifest/<manifest_id>')
def manifest(manifest_id):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = { 'error' : 'Not found' } 
    for row in db.view('id/new-view', key=id, include_docs=True):
        manifest = row['doc']

    # Delete Couch Fields
    del manifest['_id']
    del manifest['_rev']

    return manifest


@app.route('/iiif/<manifest_id>/canvas/<canvas_id_1>/<canvas_id_2>')
def canvas(manifest_id, canvas_id_1, canvas_id_2):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = None 
    for row in db.view('id/new-view', key=id, include_docs=True):
        manifest = row['doc']

    # Get Canvas
    canvas={ 'error' : 'Not found' }

    for item in manifest['items']:
        if item['id'] == 'http://localhost:3000/iiif/'+manifest_id+'/canvas/'+canvas_id_1+'/'+canvas_id_2:
            canvas = item
            break

    return canvas


# 'id':http://localhost:3000/iiif/oocihm.9_03520/annotationpage/69429/c01v5bc4998v/main
@app.route('/iiif/<manifest_id>/annotationpage/<canvas_id_1>/<canvas_id_2>/<annotationpage_id>')
def annotationpage(manifest_id, canvas_id_1, canvas_id_2, annotationpage_id):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = None 
    for row in db.view('id/new-view', key=id, include_docs=True):
        manifest = row['doc']
    

    # Get Annotation Page
    annotationpage={ 'error' : 'Not found' }

    for item in manifest['items']:
        if item['id'] == 'http://localhost:3000/iiif/'+manifest_id+'/canvas/'+canvas_id_1+'/'+canvas_id_2:
            for canvas_item in item['items']:
                if canvas_item['id'] == 'http://localhost:3000/iiif/'+manifest_id+'/annotationpage/'+canvas_id_1+'/'+canvas_id_2+'/'+annotationpage_id:
                    annotationpage = canvas_item
                    break
            else:
                continue
            break

    return annotationpage


@app.route('/iiif/<manifest_id>/annotation/<canvas_id_1>/<canvas_id_2>/<annotationpage_id>/<annotation_id>')
def annotation(manifest_id, canvas_id_1, canvas_id_2, annotationpage_id, annotation_id):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = None 
    for row in db.view('id/new-view', key=id, include_docs=True):
        manifest = row['doc']
    

    # Get Annotation
    annotation={ 'error' : 'Not found' }

    for item in manifest['items']:
        if item['id'] == 'http://localhost:3000/iiif/'+manifest_id+'/canvas/'+canvas_id_1+'/'+canvas_id_2:
            for canvas_item in item['items']:
                if canvas_item['id'] == 'http://localhost:3000/iiif/'+manifest_id+'/annotationpage/'+canvas_id_1+'/'+canvas_id_2+'/'+annotationpage_id:
                    for annotationpage_item in canvas_item['items']:
                        if annotationpage_item['id'] == 'http://localhost:3000/iiif/'+manifest_id+'/annotation/'+canvas_id_1+'/'+canvas_id_2+'/'+annotationpage_id+'/'+annotation_id:
                            annotation = annotationpage_item
                            break
                    else:
                        continue
                    break
            else:
                continue
            break

    return annotation

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)