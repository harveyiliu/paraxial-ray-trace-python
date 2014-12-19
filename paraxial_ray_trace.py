

class RefractiveSurface:
    """RefractiveSurface class - refractive surface interface description class, reference Ch. 2.4 of the Eye by G. Smith and D.A. Atchison
        Class instance variables:
            nl = refractive index for the input medium on left, a list of N surfaces
            nr = refractive index for the output medium on right, a list of N surfaces
            C = surface curvature, a list of N surfaces
        Methods:
            add_surfaces(nl, nr, C, [d]) - add surface element list with corresponding refractive indices for left and right side medium, the surface curvature, and the surface separation distance from the previous surface
            compute_surface_power() - compute the surface power for each surface in the list, in unit of [1/mm]
            trace_ray([lo]) - trace the paraxial ray using the transfer equations and calculate the image distance from the last surface apex and all the intermediate angles and heights, with optional object distance input (with negative sign)
    """

    def __init__(self, name = 'Gullstrand_Number_2_Eye'):
        # schematic eye with retina from left as the object point, IOL inside surface as surface #1
        #   IOL outside surface as surface #2, corneal inside as surface #3, image outside air
        if name.lower() == 'Gullstrand_Number_2_Eye'.lower():
            nl = [4.0/3.0, 1.416, 4.0/3.0]      #IOL index is 1.416, vitreous and aqueous index is 4/3
            nr = [1.416, 4.0/3.0, 1.0]
            C = [0.2, -0.2, -0.1282]        # curvature in unit of mm^-1
            d = [4.0, 3.2]      # separation distance between consecutive surfaces from left to right
            lo = -16.696         # object distance from retina to IOL inside surface in [mm]
        
        else:   # default to empty surface list
            nl = []
            nr = []
            C = []
            d = []
            lo = None
        
        self.nl = nl
        self.nr = nr
        self.C = C
        self.d = d
        self.lo = lo


    def add_surfaces(self, nl, nr, C, d = []):
        # add surfaces, can be list or single float value
        if type(nl) is list:
            self.nl.extend(nl)
            self.nr.extend(nr)
            self.C.extend(C)
            self.d.extend(d)
        else:
            self.nl.append(nl)
            self.nr.append(nr)
            self.C.append(C)
            if len(self.nl) > 1:
                self.d.append(d)


    def compute_surface_power(self):
        # compute the surface power for the surface list
        F = []
        for j in range(len(self.C)):
            F.append(self.C[j]*(self.nr[j] - self.nl[j]))
        return F

    def trace_ray(self, lo = None):
        if lo != None:
            self.lo = lo
        
        # trace paraxial ray to find the image distance from the last surface apex
        F = self.compute_surface_power()
        
        # seed the values for the first surface
        ul = [0.1]        # arbitrary paraxial angle for the initial object ray
        h = [-ul[0]*self.lo]
        ur = []
        for j in range(len(self.nl)):
            ur.append((-h[j]*F[j] + self.nl[j]*ul[j])/self.nr[j])     # exit angle at the jth surface
            if j < len(self.d):     # no need to transfer for the last surface
                h.append(h[j] + ur[j]*self.d[j])        # paraxial transfer function for next h
                ul.append(ur[j])    # transfer function for next angle u input

        li = -h[j]/ur[j]        # image distance from the last surface apex
        
        ray = {'li':li, 'h':h, 'ul': ul, 'ur':ur}

        return ray

