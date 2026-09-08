using UnityEngine;

public class A03ProjectionLab : MonoBehaviour
{
    [ContextMenu("Print Projection Experiment")]
    private void PrintExperiment()
    {
        float n = 1, f = 9;
        var projection = new Matrix4x4();
        projection.m00 = 1; projection.m11 = 1;
        projection.m22 = f / (n - f);
        projection.m23 = f * n / (n - f);
        projection.m32 = -1;
        Vector3[] points = {
            new Vector3(0,0,-1), new Vector3(0,0,-9),
            new Vector3(1,0,-2), new Vector3(1,0,-4)
        };
        foreach (var p in points)
        {
            Vector4 clip = projection * new Vector4(p.x,p.y,p.z,1);
            if (Mathf.Abs(clip.w) < 1e-6f) continue;
            var ndc = new Vector3(clip.x,clip.y,clip.z) / clip.w;
            Debug.Log($"View={p}, Clip={clip.ToString("F4")}, NDC={ndc.ToString("F4")}");
        }
    }
}
