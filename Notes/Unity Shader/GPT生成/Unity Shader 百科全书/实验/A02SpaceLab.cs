using UnityEngine;

public class A02SpaceLab : MonoBehaviour
{
    [ContextMenu("Print Space Experiment")]
    private void PrintExperiment()
    {
        var scale = Matrix4x4.Scale(new Vector3(2, 1, 1));
        var rotation = Matrix4x4.identity;
        rotation.m00 = 0; rotation.m01 = -1;
        rotation.m10 = 1; rotation.m11 = 0;
        var translation = Matrix4x4.Translate(new Vector3(10, 0, 0));
        var matrix = translation * rotation * scale;
        var p = new Vector3(1, 1, 0);
        Debug.Log($"Point: {matrix.MultiplyPoint3x4(p)}");
        Debug.Log($"Vector: {matrix.MultiplyVector(p)}");
        Debug.Log($"Rotation only: {rotation.MultiplyVector(p)}");
        var world = matrix.MultiplyPoint3x4(p);
        Debug.Log($"Round trip: {matrix.inverse.MultiplyPoint3x4(world)}");
    }
}
