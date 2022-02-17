import yaml

def read_nl( ):
    stream = open( "namelist.yaml", 'r' )
    return yaml.safe_load( stream )

if __name__ == "__main__":
    print( read_nl() )
