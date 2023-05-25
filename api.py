from flask import Flask
from flask_cors import CORS, cross_origin
import couchdb

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

couch = couchdb.Server('http://admin:YOURPASSWORD@couchserver:5984/')
db = couch['manifest'] 

iiif_url = "http://10.5.0.5:5000/iiif/"

@app.route('/')
def index():
    return '<p>Hello, World!</p>'

@app.route('/iiif/<collection_id>/collection')
@cross_origin()
def collection(collection_id):
    return '<p>Hello, Collection!</p>'


@app.route('/iiif/<manifest_id>/manifest')
@cross_origin()
def manifest(manifest_id):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = { 'error' : 'Not found' } 
    for row in db.view('iiif/id', key=id, include_docs=True):
        manifest = row['doc']

    # Delete Couch Fields
    if '_id' in manifest:
        del manifest['_id']
    if '_rev' in manifest:
        del manifest['_rev']

    return manifest


@app.route('/iiif/<manifest_id>/canvas/<canvas_id_1>/<canvas_id_2>')
@cross_origin()
def canvas(manifest_id, canvas_id_1, canvas_id_2):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = None 
    for row in db.view('iiif/id', key=id, include_docs=True):
        manifest = row['doc']

    # Get Canvas
    canvas={ 'error' : 'Not found' }

    for item in manifest['items']:
        if item['id'] == iiif_url+manifest_id+'/canvas/'+canvas_id_1+'/'+canvas_id_2:
            canvas = item
            break

    return canvas


@app.route('/iiif/<manifest_id>/annotationpage/<canvas_id_1>/<canvas_id_2>/<annotationpage_id>')
@cross_origin()
def annotationpage(manifest_id, canvas_id_1, canvas_id_2, annotationpage_id):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = None 
    for row in db.view('iiif/id', key=id, include_docs=True):
        manifest = row['doc']
    

    # Get Annotation Page
    annotationpage={ 'error' : 'Not found' }

    for item in manifest['items']:
        if item['id'] == iiif_url+manifest_id+'/canvas/'+canvas_id_1+'/'+canvas_id_2:
            for canvas_item in item['items']:
                if canvas_item['id'] == iiif_url+manifest_id+'/annotationpage/'+canvas_id_1+'/'+canvas_id_2+'/'+annotationpage_id:
                    annotationpage = canvas_item
                    break
            else:
                continue
            break

    return annotationpage


@app.route('/iiif/<manifest_id>/annotation/<canvas_id_1>/<canvas_id_2>/<annotationpage_id>/<annotation_id>')
@cross_origin()
def annotation(manifest_id, canvas_id_1, canvas_id_2, annotationpage_id, annotation_id):

    # Get Manifest
    id = iiif_url+manifest_id+'/manifest'
    manifest = None 
    for row in db.view('iiif/id', key=id, include_docs=True):
        manifest = row['doc']
    

    # Get Annotation
    annotation={ 'error' : 'Not found' }

    for item in manifest['items']:
        if item['id'] == iiif_url+manifest_id+'/canvas/'+canvas_id_1+'/'+canvas_id_2:
            for canvas_item in item['items']:
                if canvas_item['id'] == iiif_url+manifest_id+'/annotationpage/'+canvas_id_1+'/'+canvas_id_2+'/'+annotationpage_id:
                    for annotationpage_item in canvas_item['items']:
                        if annotationpage_item['id'] == iiif_url+manifest_id+'/annotation/'+canvas_id_1+'/'+canvas_id_2+'/'+annotationpage_id+'/'+annotation_id:
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