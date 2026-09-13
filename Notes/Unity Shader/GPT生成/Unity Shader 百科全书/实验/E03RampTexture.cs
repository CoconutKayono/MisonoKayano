using UnityEngine;

[RequireComponent(typeof(MeshRenderer))]
public class E03RampTexture : MonoBehaviour
{
    MeshRenderer target;
    Material original, owned;
    Texture2D ramp;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshRenderer>();
        original = target.sharedMaterial;
        if (original == null || !original.HasProperty("_Ramp"))
        {
            Debug.LogWarning("E03: assign the E03RampShadow material first.", this);
            return;
        }
        owned = new Material(original);
        ramp = new Texture2D(256, 2, TextureFormat.RGBA32, false, true)
        {
            name = "E03 Runtime Linear Ramp",
            wrapMode = TextureWrapMode.Clamp,
            filterMode = FilterMode.Bilinear
        };
        var pixels = new Color[256 * 2];
        for (int x = 0; x < 256; ++x)
        {
            float q = x / 255f;
            Color c = q < 0.4f ? new Color(0.08f,0.05f,0.18f,1) :
                      q < 0.7f ? new Color(0.4f,0.18f,0.2f,1) :
                                 new Color(1,0.65f,0.32f,1);
            pixels[x] = pixels[256 + x] = c;
        }
        ramp.SetPixels(pixels);
        ramp.Apply(false, false);
        owned.SetTexture("_Ramp", ramp);
        target.sharedMaterial = owned;
    }
    void OnDisable()
    {
        if (target != null && owned != null && target.sharedMaterial == owned)
            target.sharedMaterial = original;
        if (owned != null) Destroy(owned);
        if (ramp != null) Destroy(ramp);
        owned = null;
        ramp = null;
    }
}
