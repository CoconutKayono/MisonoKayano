using UnityEngine;

public class A07BufferLab : MonoBehaviour
{
    [ContextMenu("Run Buffer Upload Example")]
    public void Run()
    {
        const int count = 4;
        const int stride = 4 * sizeof(float);
        var data = new Vector4[]
        {
            new Vector4(1, 0, 0, 1),
            new Vector4(0, 1, 0, 1),
            new Vector4(0, 0, 1, 1),
            new Vector4(1, 1, 1, 1)
        };
        using (var buffer = new GraphicsBuffer(
            GraphicsBuffer.Target.Structured, count, stride))
        {
            buffer.SetData(data);
            var patch = new Vector4[] { new Vector4(0.25f, 0.5f, 1, 1) };
            buffer.SetData(patch, 0, 2, 1);
            Debug.Log($"Resource payload: {count * stride} B; " +
                      $"full update: {count * stride} B; partial update: {stride} B.");
            Debug.Log("SetData returned. No draw or readback was requested.");
        }
    }
}
