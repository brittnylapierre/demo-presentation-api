# Python program to read
# json file
import ijson
import json
  
iiif_url = "http://10.5.0.5:5000/iiif/"

def iiif_annotation(manifest, image):
  return {
    'id'         : iiif_url+manifest['slug']+'/annotation/'+image['id']+"/main/image",
    'type'       : 'Annotation',
    'motivation' : 'painting',
    'body'       : {
      'id'       : 'https://image-tor.canadiana.ca/iiif/2/'+image['id']+'/full/max/0/default.jpg',
      'type'     : 'Image',
      'format'   : 'image/jpeg',
      'service'  : [ {
          'id'      : 'https://image-tor.canadiana.ca/iiif/2/'+image['id'],
          'type'    : 'ImageService2',
          'profile' : 'level2'
        }
      ],
      'height' : image['canonicalMasterHeight'],
      'width'  : image['canonicalMasterWidth']
    },
    'target'   : iiif_url+manifest['slug']+'/canvas/'+image['id']
  }

def iiif_annotation_page(manifest, image):
  annotation = iiif_annotation(manifest, image)
  return {
    'id'    : iiif_url+manifest['slug']+'/annotationpage/'+image['id']+"/main",
    'type'  : 'AnnotationPage',
    'items' : [ annotation ]
  }

def iiif_thumbnail(image):
  return {
    'id'     : 'https://image-tor.canadiana.ca/iiif/2/'+image['id']+'/full/max/0/default.jpg',
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

  return {
    '@context' : 'https://iiif.io/api/presentation/3/context.json',
    'id'       : iiif_url+manifest['slug']+'/manifest',
    'type'     : 'Manifest',
    'label'    : { 'none' : [ manifest['label'] ]},
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
      manifest = row['doc']

      if 'canvases' in manifest:
        images = []
        # 'canvases':[{'id':'69429/c0cc0ts7gj64','label':{'none':'Image 1'}} ... ]
        for canvas in manifest['canvases']:
          images.append( {
            'id'                    : canvas['id'], # todo url escape
            'label'                 : canvas['label'],
            'canonicalMasterHeight' : 0, # todo
            'canonicalMasterWidth'  : 0
          })
        manifest_json = iiif_manifest(manifest, images)
        #print(manifest_json)
        f = open('./manifests/' + manifest['slug'] + '.json', 'w')
        manifest_str = json.dumps(manifest_json)
        f.write(manifest_str)
        f.close()

