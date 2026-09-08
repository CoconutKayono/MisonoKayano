using UnityEngine;

[RequireComponent(typeof(Renderer))]
public class B06TextureLab : MonoBehaviour
{
    public Shader labShader;
    public bool mipChain=true;
    public FilterMode filter=FilterMode.Trilinear;
    [Range(1,16)] public int anisotropy=1;
    [Range(0,3)] public int mode=0;
    [Range(1,32)] public float tiling=8;
    Renderer rendererComponent;
    Material previousMaterial, ownedMaterial;
    Texture2D texture;
    void Start()
    {
        if(labShader==null || !labShader.isSupported) { enabled=false; return; }
        rendererComponent=GetComponent<Renderer>();
        previousMaterial=rendererComponent.sharedMaterial;
        ownedMaterial=new Material(labShader);
        rendererComponent.sharedMaterial=ownedMaterial;
        Rebuild();
    }
    [ContextMenu("Rebuild Checker Texture")]
    public void Rebuild()
    {
        if(!Application.isPlaying || ownedMaterial==null) return;
        if(texture!=null) Destroy(texture);
        texture=new Texture2D(256,256,TextureFormat.RGBA32,mipChain,true);
        texture.name="B06 Owned Checker";
        texture.wrapMode=TextureWrapMode.Repeat;
        var pixels=new Color32[256*256];
        for(int y=0;y<256;y++) for(int x=0;x<256;x++)
        {
            byte v=(byte)(((x/8+y/8)%2)*255);
            pixels[y*256+x]=new Color32(v,v,v,255);
        }
        texture.SetPixels32(pixels);
        texture.Apply(true,false);
        ownedMaterial.SetTexture("_MainTex",texture);
    }
    void Update()
    {
        if(texture==null || ownedMaterial==null) return;
        texture.filterMode=filter;
        texture.anisoLevel=anisotropy;
        ownedMaterial.SetFloat("_Mode",mode);
        ownedMaterial.SetFloat("_Tiling",tiling);
    }
    void OnDestroy()
    {
        if(rendererComponent!=null && rendererComponent.sharedMaterial==ownedMaterial)
            rendererComponent.sharedMaterial=previousMaterial;
        if(texture!=null) Destroy(texture);
        if(ownedMaterial!=null) Destroy(ownedMaterial);
    }
}
