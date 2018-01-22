# updates S3 Single Page Application js/config.js with API Gateway Url

  import json
  import boto3
  import cfnresponse

  s3 = boto3.resource('s3')

  def create(properties, physical_id):
    bucket = properties['Bucket']
    config_object = s3.Object(bucket, 'js/config.js').get()
    config_data = config_object["Body"].read()
    config_data = config_data.replace("Base URL of your API including the stage", properties["InvokeUrl"])
    config = s3.Object(bucket,'js/config.js')
    config.put(Body=config_data)
    return cfnresponse.SUCCESS, None

  def update(properties, physical_id):
    return create(properties, physical_id)

  def delete(properties, physical_id):
    return cfnresponse.SUCCESS, physical_id

  def handler(event, context):
    print "Received event: %s" % json.dumps(event)

    status = cfnresponse.FAILED
    new_physical_id = None

    try:
      properties = event.get('ResourceProperties')
      physical_id = event.get('PhysicalResourceId')

      status, new_physical_id = {
        'Create': create,
        'Update': update,
        'Delete': delete
      }.get(event['RequestType'], lambda x, y: (cfnresponse.FAILED, None))(properties, physical_id)
    except Exception as e:
      print "Exception: %s" % e
      status = cfnresponse.FAILED
    finally:
      cfnresponse.send(event, context, status, {}, new_physical_id)