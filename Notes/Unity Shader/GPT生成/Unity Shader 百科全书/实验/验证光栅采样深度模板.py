"""B05-B08 mathematical examples. Not GPU rasterization or synchronization tests."""
import math
import unittest


def perspective(values, weights, ws):
    return sum(a*l/w for a,l,w in zip(values,weights,ws)) / sum(l/w for l,w in zip(weights,ws))


def lerp(a,b,t):
    return a+(b-a)*t


def smoothstep(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)))
    return t*t*(3-2*t)


def depth(z,n=0.1,f=100):
    return f/(f-n)-f*n/((f-n)*z)


def eye(d,n=0.1,f=100):
    return f*n/(f-d*(f-n))


def reverse_eye(d,n=0.1,f=100):
    return f*n/(n+d*(f-n))


def depth_step(stored,incoming,test,write):
    passed = test=='Always' or (test=='LEqual' and incoming<=stored)
    return passed, incoming if passed and write else stored


def stencil_compare(ref,stored,mask,comparison):
    left,right=ref&mask,stored&mask
    return {'Always':True,'Never':False,'Equal':left==right,'NotEqual':left!=right,
            'Less':left<right,'Greater':left>right}[comparison]


def stencil_op(stored,ref,write_mask,operation):
    candidate={'Keep':stored,'Zero':0,'Replace':ref,'Invert':stored^255,
               'IncrSat':min(255,stored+1),'IncrWrap':(stored+1)&255}[operation]
    return (stored&(255^write_mask)) | (candidate&write_mask)


def stencil_step(stored,ref,read_mask,write_mask,comparison,z_pass):
    passed=stencil_compare(ref,stored,read_mask,comparison)
    op='Zero' if not passed else ('Replace' if z_pass else 'Invert')
    return op,stencil_op(stored,ref,write_mask,op)


class RasterSamplingDepthStencil(unittest.TestCase):
    def test_barycentric_reconstruction(self):
        points=[(0,0),(2,0),(0,2)]
        weights=[0.2,0.3,0.5]
        self.assertAlmostEqual(sum(weights),1)
        self.assertEqual(tuple(sum(p[k]*w for p,w in zip(points,weights)) for k in (0,1)),(0.6,1.0))

    def test_perspective_screen_midpoint(self):
        self.assertAlmostEqual(perspective([0,1],[0.5,0.5],[1,4]),0.2)
        self.assertEqual(lerp(0,1,0.5),0.5)

    def test_equal_w_and_affine_pack(self):
        uv=[0,1,1]; weights=[0.25,0.25,0.5]; ws=[1,2,4]
        expected=sum(a*l for a,l in zip(uv,weights))
        self.assertEqual(perspective(uv,weights,[2,2,2]),expected)
        packed=perspective([a*w for a,w in zip(uv,ws)],weights,ws)
        interpolated_w=perspective(ws,weights,ws)
        self.assertEqual(packed/interpolated_w,expected)
        self.assertEqual(perspective(uv,weights,ws),0.5)

    def test_quad_difference_and_threshold(self):
        dx=0.12-0.10; dy=0.13-0.10
        width=abs(dx)+abs(dy)
        self.assertAlmostEqual(width,0.05)
        self.assertAlmostEqual(smoothstep(0.5-width/2,0.5+width/2,0.5),0.5)
        self.assertEqual(smoothstep(0.475,0.525,0.4),0)
        self.assertEqual(smoothstep(0.475,0.525,0.6),1)

    def test_texel_center_and_bilinear(self):
        self.assertEqual((2+0.5)/4,0.625)
        self.assertEqual(lerp(lerp(0,1,0.5),lerp(1,0,0.5),0.5),0.5)
        self.assertEqual(lerp(lerp(0,1,0.25),lerp(1,0,0.25),0.75),0.625)

    def test_lod_and_trilinear(self):
        gx=(1024/256,0); gy=(0,1024/1024)
        rho=max(math.hypot(*gx),math.hypot(*gy))
        self.assertEqual(math.log2(rho),2)
        self.assertAlmostEqual(lerp(0.2,0.8,2.25-2),0.35)

    def test_frac_discontinuity(self):
        continuous=1.01-0.99
        wrapped=(1.01%1)-(0.99%1)
        self.assertAlmostEqual(continuous,0.02)
        self.assertAlmostEqual(wrapped,-0.98)
        self.assertAlmostEqual(abs(wrapped/continuous),49)
        self.assertAlmostEqual(math.log2(abs(wrapped/continuous)),5.614709844115208)

    def test_depth_endpoints(self):
        self.assertAlmostEqual(depth(0.1),0)
        self.assertAlmostEqual(depth(100),1)
        self.assertAlmostEqual(depth(1),0.9009009009009008)
        self.assertAlmostEqual(depth(10),0.9909909909909909)

    def test_depth_inverse_and_reversed(self):
        for z in (0.1,0.2,1,10,50,100):
            self.assertAlmostEqual(eye(depth(z)),z,places=9)
            self.assertAlmostEqual(reverse_eye(1-depth(z)),z,places=9)
        self.assertAlmostEqual(eye(0.5),0.1998001998001998)

    def test_eye_distance_orthographic_and_linear01(self):
        self.assertEqual(math.hypot(3,4),5)
        self.assertEqual(lerp(0.1,100,0.5),50.05)
        self.assertEqual(0.1/100,0.001)  # Near is not zero for z/f.

    def test_depth_write_is_separate(self):
        self.assertEqual(depth_step(0.4,0.7,'LEqual',False),(False,0.4))
        self.assertEqual(depth_step(0.4,0.2,'LEqual',False),(True,0.4))
        self.assertEqual(depth_step(0.4,0.2,'LEqual',True),(True,0.2))
        self.assertEqual(depth_step(0.4,0.7,'Always',True),(True,0.7))

    def test_reversed_comparison_equivalence(self):
        for stored,new in ((0.4,0.7),(0.4,0.2),(0.4,0.4)):
            self.assertEqual(new<=stored,1-new>=1-stored)

    def test_unorm_depth_error_model(self):
        b=100*0.1/(100-0.1)
        delta=1/(2**24-1)
        self.assertAlmostEqual((100**2*delta/b)/(10**2*delta/b),100)
        self.assertAlmostEqual(10**2*delta/b,0.00005954504367977689)
        codes=[q/255 for q in range(256)]
        self.assertTrue(all(abs(a-b)<1e-15 for a,b in zip(codes,sorted(1-d for d in codes))))

    def test_stencil_compare_direction(self):
        self.assertTrue(stencil_compare(3,5,255,'Less'))
        self.assertFalse(stencil_compare(5,3,255,'Less'))

    def test_stencil_read_mask(self):
        self.assertTrue(stencil_compare(8,10,8,'Equal'))
        self.assertFalse(stencil_compare(8,10,255,'Equal'))
        self.assertTrue(stencil_compare(8,10,0,'Equal'))
        self.assertFalse(stencil_compare(8,10,0,'NotEqual'))

    def test_stencil_write_mask(self):
        self.assertEqual(stencil_op(170,4,15,'Replace'),164)
        self.assertEqual(stencil_op(170,0,0,'Zero'),170)
        self.assertEqual(stencil_op(7,0,8,'IncrWrap'),15)

    def test_stencil_saturation_wrap(self):
        self.assertEqual(stencil_op(255,0,255,'IncrSat'),255)
        self.assertEqual(stencil_op(255,0,255,'IncrWrap'),0)

    def test_stencil_three_paths(self):
        self.assertEqual(stencil_step(0,8,8,8,'Always',True),('Replace',8))
        self.assertEqual(stencil_step(8,8,8,8,'Never',True),('Zero',0))
        self.assertEqual(stencil_step(8,8,8,8,'Always',False),('Invert',0))

    def test_writer_reader_order(self):
        initial=0
        read=lambda s: stencil_compare(8,s,8,'Equal')
        self.assertFalse(read(initial))
        updated=stencil_step(initial,8,8,8,'Always',True)[1]
        self.assertTrue(read(updated))
        # A new frame clears to the same initial state; no feedback accumulation.
        self.assertFalse(read(initial))


if __name__=='__main__':
    unittest.main(verbosity=2)
