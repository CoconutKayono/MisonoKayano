using UnityEngine;

public class A04NormalLab : MonoBehaviour
{
    [ContextMenu("Print Normal Experiment")]
    private void PrintExperiment()
    {
        var matrix = Matrix4x4.Scale(new Vector3(2,1,1));
        var n = new Vector3(1,1,0);
        var t = new Vector3(1,-1,0);
        Vector3 transformedTangent = matrix.MultiplyVector(t).normalized;
        Vector3 wrong = matrix.MultiplyVector(n).normalized;
        Vector3 correct = matrix.inverse.transpose.MultiplyVector(n).normalized;
        Debug.Log($"Wrong perpendicularity: {Vector3.Dot(wrong,transformedTangent):F6}");
        Debug.Log($"Correct perpendicularity: {Vector3.Dot(correct,transformedTangent):F6}");
        Debug.Log($"Wrong N dot Y: {Vector3.Dot(wrong,Vector3.up):F6}");
        Debug.Log($"Correct N dot Y: {Vector3.Dot(correct,Vector3.up):F6}");
    }
}
