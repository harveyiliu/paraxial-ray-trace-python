#!/usr/bin/python
import paraxial_ray_trace as prt


if __name__ == "__main__":
    """ Paraxial ray trace through a set of refractive surfaces demo
            Input arguments:
                modelName = predefined model name, current set of models are:
                    1. Gullstrand_Number_2_Eye - default
        Run command example:
            ./paraxial_ray_trace_demo.py Gullstrand_Number_2_Eye &      
    """
    
    import sys
    modelName = sys.argv[1]     # refractive surface system model name
    model = prt.RefractiveSurface(modelName)
    ray = model.trace_ray()
    print '\n', ray
    
    
