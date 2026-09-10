using UnityEngine;

public class A05ColorLab : MonoBehaviour
{
    private static double Decode(double e) => e <= 0.04045
        ? e / 12.92 : System.Math.Pow((e + 0.055) / 1.055, 2.4);
    private static double Encode(double l) => l <= 0.0031308
        ? 12.92 * l : 1.055 * System.Math.Pow(l, 1.0 / 2.4) - 0.055;

    [ContextMenu("Print Color Experiment")]
    private void PrintExperiment()
    {
        Debug.Log($"Decode 0.5: {Decode(0.5):F6}");
        Debug.Log($"Encode 0.5: {Encode(0.5):F6}");
        Debug.Log($"Double decode: {Decode(Decode(0.5)):F6}");
        Debug.Log($"Byte 128 decoded: {Decode(128.0 / 255.0):F6}");
        Debug.Log($"Linear 0.5 nearest byte: {System.Math.Round(Encode(0.5)*255)}");
        Debug.Log($"Teaching HDR mapping: {Encode(4.0/(1.0+4.0)):F6}");
    }
}
