using UnityEngine;

[RequireComponent(typeof(MeshFilter))]
public class A06MeshAudit : MonoBehaviour
{
    [ContextMenu("Print Mesh Layout")]
    private void PrintLayout()
    {
        Mesh mesh = GetComponent<MeshFilter>().sharedMesh;
        if (mesh == null) { Debug.Log("No mesh assigned."); return; }
        Debug.Log($"Mesh={mesh.name}, Vertices={mesh.vertexCount}, SubMeshes={mesh.subMeshCount}, IndexFormat={mesh.indexFormat}, Readable={mesh.isReadable}");
        long logicalVertexBytes = 0;
        for (int stream = 0; stream < mesh.vertexBufferCount; stream++)
        {
            int stride = mesh.GetVertexBufferStride(stream);
            logicalVertexBytes += (long)mesh.vertexCount * stride;
            Debug.Log($"Stream {stream}: stride={stride}");
        }
        foreach (var attribute in mesh.GetVertexAttributes())
        {
            int offset = mesh.GetVertexAttributeOffset(attribute.attribute);
            Debug.Log($"{attribute.attribute}: {attribute.format} x{attribute.dimension}, stream={attribute.stream}, offset={offset}");
        }
        for (int sub = 0; sub < mesh.subMeshCount; sub++)
            Debug.Log($"SubMesh {sub}: topology={mesh.GetTopology(sub)}, indexCount={mesh.GetIndexCount(sub)}, baseVertex={mesh.GetBaseVertex(sub)}");
        Debug.Log($"Logical vertex bytes={logicalVertexBytes}; excludes allocation overhead and other mesh data.");
    }
}
