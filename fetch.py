from transform import Transform
from validate import Validate

# performs the pipeline for fetching and validating data
#transforms the data and adds it to the database
transform = Transform()
transform.transformNational()
transform.transformRegional()
#validates the data
validate = Validate()
validate.validate()