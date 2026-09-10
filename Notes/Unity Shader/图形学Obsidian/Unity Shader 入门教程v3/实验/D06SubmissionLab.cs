using UnityEngine;
using UnityEngine.Rendering;

public class D06SubmissionLab : MonoBehaviour
{
    public enum Submission { Renderers, ExplicitInstancing }
    public Submission submission;
    [Range(1, 20)] public int side = 10;
    public Material sourceMaterial;
    public Camera targetCamera;
    GameObject generatedRoot;
    Material ownedMaterial;
    Mesh mesh;
    Matrix4x4[] matrices;
    Submission builtSubmission;

    void OnEnable() { if (Application.isPlaying) Rebuild(); }

    [ContextMenu("Rebuild")]
    public void Rebuild()
    {
        if (!Application.isPlaying) return;
        Cleanup();
        builtSubmission = submission;
        if (sourceMaterial == null || targetCamera == null)
        {
            Debug.LogWarning("D06: assign a URP/Lit material and the single Game Camera.", this);
            return;
        }
        if (submission == Submission.ExplicitInstancing && !SystemInfo.supportsInstancing)
        {
            Debug.LogWarning("D06: this device does not support instancing.", this);
            return;
        }
        ownedMaterial = new Material(sourceMaterial) { enableInstancing = true };
        generatedRoot = new GameObject("D06 Generated");
        generatedRoot.transform.SetParent(transform, false);
        var template = GameObject.CreatePrimitive(PrimitiveType.Cube);
        template.name = "D06 Mesh Source (inactive)";
        template.transform.SetParent(generatedRoot.transform, false);
        mesh = template.GetComponent<MeshFilter>().sharedMesh;
        template.SetActive(false);
        int n = Mathf.Clamp(side, 1, 20);
        matrices = new Matrix4x4[n * n];
        for (int z = 0; z < n; ++z)
        for (int x = 0; x < n; ++x)
        {
            var localPosition = new Vector3((x - (n - 1) * 0.5f) * 1.4f, 0,
                                           (z - (n - 1) * 0.5f) * 1.4f);
            matrices[z * n + x] = transform.localToWorldMatrix *
                Matrix4x4.TRS(localPosition, Quaternion.identity, Vector3.one);
            if (submission != Submission.Renderers) continue;
            var item = new GameObject("D06 Cube " + (z * n + x));
            item.transform.SetParent(generatedRoot.transform, false);
            item.transform.localPosition = localPosition;
            item.AddComponent<MeshFilter>().sharedMesh = mesh;
            var r = item.AddComponent<MeshRenderer>();
            r.sharedMaterial = ownedMaterial;
            r.shadowCastingMode = ShadowCastingMode.Off;
            r.receiveShadows = false;
            r.lightProbeUsage = LightProbeUsage.Off;
            r.reflectionProbeUsage = ReflectionProbeUsage.Off;
        }
    }
    void Update()
    {
        if (submission != builtSubmission) Rebuild();
        if (submission != Submission.ExplicitInstancing || matrices == null || ownedMaterial == null) return;
        var rp = new RenderParams(ownedMaterial)
        {
            camera = targetCamera,
            shadowCastingMode = ShadowCastingMode.Off,
            receiveShadows = false,
            lightProbeUsage = LightProbeUsage.Off,
            reflectionProbeUsage = ReflectionProbeUsage.Off
        };
        Graphics.RenderMeshInstanced(rp, mesh, 0, matrices);
    }
    void OnDisable() { Cleanup(); }
    void Cleanup()
    {
        if (generatedRoot != null)
        {
            generatedRoot.SetActive(false);
            Destroy(generatedRoot);
        }
        if (ownedMaterial != null) Destroy(ownedMaterial);
        generatedRoot = null;
        ownedMaterial = null;
        matrices = null;
        mesh = null;
    }
}
