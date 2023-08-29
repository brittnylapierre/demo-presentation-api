import couchdb
import ijson
import pandas

# Before Running:
'''
docker compose up -d

cd setup

# Curl download canvases to json
# curl -X GET http://<YOURUSER>:<YOURPASSWORD>@<url>:5984/canvas/_all_docs?include_docs=true > ./canvases.json

python3 parseCanvases.py

# Curl download access to json
# curl -X GET http://<YOURUSER>:<YOURPASSWORD>@<url>:5984/access/_all_docs?include_docs=true > ./accessdb.json

python3 loadManifestsIntoDB.py
'''

print("Start!")

p = pandas.read_json('canvascleaned.json', orient="index")

couch = couchdb.Server("http://admin:YOURPASSWORD@localhost:5984/")
db = couch["manifest"]

iiif_url = "http://10.5.0.5:5000/iiif/"
image_server_url = 'https://image-tor.canadiana.ca/iiif/2/'

def iiif_annotation(manifest, image):
  parsed_id = image['id'].replace("/", "%2f")
  return {
    'id'         : iiif_url+manifest['slug']+'/annotation/'+image['id']+"/main/image",
    'type'       : 'Annotation',
    'motivation' : 'painting',
    'body'       : {
      'id'       : image_server_url+parsed_id+'/full/max/0/default.jpg',
      'type'     : 'Image',
      'format'   : 'image/jpeg',
      'service'  : [ {
          'id'      : image_server_url+parsed_id,
          'type'    : 'ImageService2',
          'profile' : 'level2'
        }
      ],
      'height' : image['canonicalMasterHeight'],
      'width'  : image['canonicalMasterWidth']
    },
    'target'   : iiif_url+manifest['slug']+'/canvas/'+parsed_id
  }

def iiif_annotation_page(manifest, image):
  annotation = iiif_annotation(manifest, image)
  return {
    'id'    : iiif_url+manifest['slug']+'/annotationpage/'+image['id']+"/main",
    'type'  : 'AnnotationPage',
    'items' : [ annotation ]
  }

def iiif_thumbnail(image):
  parsed_id = image['id'].replace("/", "%2f")
  return {
    'id'     : image_server_url+parsed_id+'/full/max/0/default.jpg',
    'type'   : 'Image',
    'format' : 'image/jpeg'
  }

def iiif_canvas(manifest, image): 
  thumbnail = iiif_thumbnail(image)
  annotation_page = iiif_annotation_page(manifest, image)
  return {
    'id'     : iiif_url+manifest['slug']+'/canvas/'+image['id'],
    'type'   : 'Canvas',
    'label'  : { 'none' : [ image['label'] ] },
    'height' : image['canonicalMasterHeight'],
    'width'  : image['canonicalMasterWidth'],
    'thumbnail' : [ thumbnail ],
    'items'  : [ annotation_page ],
  }



def iiif_manifest(manifest, images):
  
  items = []
  for image in images:
    items.append(iiif_canvas(manifest,image))

  label = "No label set"
  if 'label' in manifest and 'none' in manifest['label']:
    label = manifest['label']['none']

  return {
    '@context' : 'https://iiif.io/api/presentation/3/context.json',
    'id'       : iiif_url+manifest['slug']+'/manifest',
    'type'     : 'Manifest',
    'label'    : { 'none' : [ label ]},
    'provider' : [ {
        'id'    : 'https://www.crkn-rcdr.ca/',
        'type'  : 'Agent',
        'label' : {
          'en' : ['Canadian Research Knowledge Network'],
          'fr' : ['Réseau canadien de documentation pour la recherche']
        },
        'homepage' : [{
          'id'    : 'https://www.crkn-rcdr.ca/',
          'type'  : 'Text',
          'label' : {
            'en' : ['Canadian Research Knowledge Network'],
            'fr' : ['Réseau canadien de documentation pour la recherche']
          },
          'format' : 'text/html'
        }]
      }
    ],
    'metadata' : [],
    'items'    : items
  }



# Iterating through the json
with open('accessdb.json', 'rb') as f:
  for row in ijson.items(f, 'rows.item'):
    try:
      manifest = row['doc']
      if 'canvases' in manifest:
        images = []

        for canvas in manifest['canvases']:

          width = int(p.loc[canvas["id"]][0])
          height = int(p.loc[canvas["id"]][1])

          label = "image"
          if 'label' in canvas and 'none' in canvas['label']:
            label = canvas['label']['none']

          images.append( {
            'id'                    : canvas['id'], # todo url escape
            'label'                 : label,
            'canonicalMasterHeight' : width,
            'canonicalMasterWidth'  : height
          })

        manifest_json = iiif_manifest(manifest, images)
        db.save(manifest_json)
      
    except Exception as e: print(e)

print("Done!")