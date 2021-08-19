import yaml

def read_nl( ):
    stream = open( "namelist.yaml", 'r' )
    return yaml.safe_load( stream )

## Maybe add a function to reset nl to default values

if __name__ == "__main__":
    print( read_nl() )