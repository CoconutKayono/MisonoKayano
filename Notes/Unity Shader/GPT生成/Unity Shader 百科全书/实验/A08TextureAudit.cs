using UnityEditor;
using UnityEngine;

public static class A08TextureAudit
{
    [MenuItem("Tools/Encyclopedia/A08 Audit Selected Texture")]
    public static void Audit()
    {
        var texture = Selection.activeObject as Texture2D;
        if (texture == null)
        {
            Debug.LogWarning("Select an imported Texture2D in the Project window.");
            return;
        }
        string path = AssetDatabase.GetAssetPath(texture);
        var importer = AssetImporter.GetAtPath(path) as TextureImporter;
        Debug.Log($"{path}\nSize={texture.width}x{texture.height}, " +
                  $"Format={texture.graphicsFormat}, Mips={texture.mipmapCount}, " +
                  $"Readable={texture.isReadable}");
        if (importer != null)
            Debug.Log($"Type={importer.textureType}, sRGB={importer.sRGBTexture}, " +
                      $"MipsRequested={importer.mipmapEnabled}, " +
                      $"CompressionSetting={importer.textureCompression}");
        Debug.Log("This describes the current Editor texture, not a device memory measurement.");
    }
}
