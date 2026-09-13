using UnityEngine;

[RequireComponent(typeof(MeshRenderer))]
public class E06MatCapTexture : MonoBehaviour
{
    MeshRenderer target;
    Material original, owned;
    Texture2D texture;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshRenderer>();
        original = target.sharedMaterial;
        if (original == null || !original.HasProperty("_MatCap")) return;
        owned = new Material(original);
        const int size = 128;
        texture = new Texture2D(size,size,TextureFormat.RGBA32,false,true)
        {
            name = "E06 Runtime MatCap",
            filterMode = FilterMode.Bilinear,
            wrapMode = TextureWrapMode.Clamp
        };
        var pixels = new Color[size*size];
        for (int y=0; y<size; ++y)
        for (int x=0; x<size; ++x)
        {
            float u=(x+0.5f)/size, v=(y+0.5f)/size;
            float dx=u-0.35f, dy=v-0.75f;
            float spot=Mathf.Exp(-(dx*dx/0.012f+dy*dy/0.025f));
            float band=Mathf.Exp(-Mathf.Pow((v-0.35f)/0.07f,2));
            Color c=new Color(0.08f,0.12f,0.2f,1)*(1-0.7f*band) +
                    new Color(0.9f,0.8f,0.55f,0)*spot;
            c.a=1;
            pixels[y*size+x]=c;
        }
        texture.SetPixels(pixels);
        texture.Apply(false,false);
        owned.SetTexture("_MatCap",texture);
        target.sharedMaterial=owned;
    }
    void OnDisable()
    {
        if(target!=null && owned!=null && target.sharedMaterial==owned) target.sharedMaterial=original;
        if(owned!=null) Destroy(owned);
        if(texture!=null) Destroy(texture);
        owned=null; texture=null;
    }
}
