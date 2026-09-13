using UnityEngine;

[RequireComponent(typeof(MeshRenderer))]
public class E04FaceFieldBinding : MonoBehaviour
{
    public Transform headFrame;
    MeshRenderer target;
    Material original, owned;
    Texture2D map;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshRenderer>();
        original = target.sharedMaterial;
        if (headFrame == null || original == null || !original.HasProperty("_FaceMap"))
        {
            Debug.LogWarning("E04: assign HeadFrame and the E04FaceField material.", this);
            return;
        }
        owned = new Material(original);
        const int size = 256;
        map = new Texture2D(size,size,TextureFormat.RGBA32,false,true)
        {
            name = "E04 Angle Threshold And Circle Distance",
            filterMode = FilterMode.Bilinear,
            wrapMode = TextureWrapMode.Clamp
        };
        var pixels = new Color[size * size];
        for (int y = 0; y < size; ++y)
        for (int x = 0; x < size; ++x)
        {
            float u = (x + 0.5f) / size;
            float v = (y + 0.5f) / size;
            float px = u - 0.5f, py = v - 0.55f;
            float nose = 0.18f * Mathf.Exp(-(px*px/0.008f + py*py/0.04f));
            float threshold = Mathf.Clamp(0.15f + 0.7f*u + nose,0.05f,0.95f);
            float distance = 0.3f - new Vector2(u - 0.5f,v - 0.5f).magnitude;
            float encodedDistance = Mathf.Clamp01(0.5f + distance / 0.5f);
            float ex = (u - 0.5f) / 0.42f, ey = (v - 0.5f) / 0.48f;
            float area = ex*ex + ey*ey <= 1 ? 1 : 0;
            pixels[y*size+x] = new Color(threshold,encodedDistance,0,area);
        }
        map.SetPixels(pixels);
        map.Apply(false,false);
        owned.SetTexture("_FaceMap",map);
        target.sharedMaterial = owned;
        UpdateFrame();
    }
    void LateUpdate() { UpdateFrame(); }
    void UpdateFrame()
    {
        if (owned == null || headFrame == null) return;
        Vector3 r = headFrame.right.normalized;
        Vector3 f = headFrame.forward.normalized;
        owned.SetVector("_HeadRightWS",new Vector4(r.x,r.y,r.z,0));
        owned.SetVector("_HeadForwardWS",new Vector4(f.x,f.y,f.z,0));
    }
    void OnDisable()
    {
        if (target != null && owned != null && target.sharedMaterial == owned)
            target.sharedMaterial = original;
        if (owned != null) Destroy(owned);
        if (map != null) Destroy(map);
        owned = null;
        map = null;
    }
}
