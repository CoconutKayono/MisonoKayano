using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter))]
public class E05NormalStreams : MonoBehaviour
{
    MeshFilter target;
    Mesh original, owned;
    void OnEnable()
    {
        if (!Application.isPlaying) return;
        target = GetComponent<MeshFilter>();
        original = target.sharedMesh;
        if (original == null || !original.isReadable)
        {
            Debug.LogWarning("E05: use a readable triangle mesh, such as the built-in Cube.", this);
            return;
        }
        Vector3[] p = original.vertices;
        Vector3[] oldNormals = original.normals;
        if (oldNormals.Length != p.Length) return;
        int[] triangles = original.triangles;
        var sums = new Dictionary<Vector3, Vector3>();
        for (int k = 0; k < triangles.Length; k += 3)
        {
            int a = triangles[k], b = triangles[k+1], c = triangles[k+2];
            Vector3 face = Vector3.Cross(p[b]-p[a], p[c]-p[a]);
            if (face.sqrMagnitude < 1e-16f) continue;
            face.Normalize();
            Add(sums, p[a], face * Vector3.Angle(p[b]-p[a], p[c]-p[a]) * Mathf.Deg2Rad);
            Add(sums, p[b], face * Vector3.Angle(p[c]-p[b], p[a]-p[b]) * Mathf.Deg2Rad);
            Add(sums, p[c], face * Vector3.Angle(p[a]-p[c], p[b]-p[c]) * Mathf.Deg2Rad);
        }
        var smooth = new List<Vector3>(p.Length);
        var artistic = new List<Vector3>(p.Length);
        for (int i = 0; i < p.Length; ++i)
        {
            Vector3 n;
            if (!sums.TryGetValue(p[i], out n) || n.sqrMagnitude < 1e-12f)
                n = oldNormals[i];
            n.Normalize();
            smooth.Add(n);
            artistic.Add(new Vector3(n.x, n.y * 0.2f, n.z).normalized);
        }
        owned = Instantiate(original);
        owned.name = "E05 Private Direction Streams";
        owned.SetUVs(3, smooth);
        owned.SetUVs(2, artistic);
        target.sharedMesh = owned;
    }
    static void Add(Dictionary<Vector3,Vector3> sums, Vector3 position, Vector3 value)
    {
        Vector3 sum;
        sums.TryGetValue(position, out sum);
        sums[position] = sum + value;
    }
    void OnDisable()
    {
        if (target != null && owned != null && target.sharedMesh == owned)
            target.sharedMesh = original;
        if (owned != null) Destroy(owned);
        owned = null;
    }
}
