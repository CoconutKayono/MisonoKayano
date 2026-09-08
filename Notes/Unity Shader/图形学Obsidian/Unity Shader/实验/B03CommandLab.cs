using UnityEngine;
using UnityEngine.Rendering;

public class B03CommandLab : MonoBehaviour
{
    public Shader labShader;
    public bool execute = true;
    public bool drawTriangle = true;
    RenderTexture target;
    Mesh mesh;
    Material material;
    CommandBuffer commands;

    void Start()
    {
        if (labShader == null || !labShader.isSupported)
        {
            Debug.LogError("Assign the supported B03ClipTriangle shader.");
            enabled = false;
            return;
        }
        material = new Material(labShader);
        mesh = new Mesh { name = "B03 Owned Triangle" };
        mesh.vertices = new Vector3[] {
            new Vector3(-0.8f,-0.7f,0.5f),
            new Vector3(0,0.8f,0.5f),
            new Vector3(0.8f,-0.7f,0.5f) };
        mesh.triangles = new int[] { 0, 1, 2 };
        target = new RenderTexture(128,128,0,RenderTextureFormat.ARGB32);
        target.name = "B03 Owned Target";
        target.Create();
        commands = new CommandBuffer { name = "B03 Record Versus Execute" };
    }
    void Update()
    {
        if (commands == null) return;
        commands.Clear();
        commands.SetRenderTarget(target);
        commands.SetViewport(new Rect(0,0,128,128));
        commands.ClearRenderTarget(false,true,Color.black);
        if (drawTriangle)
            commands.DrawMesh(mesh,Matrix4x4.identity,material,0,0);
        if (execute)
            Graphics.ExecuteCommandBuffer(commands);
    }
    void OnGUI()
    {
        if (target != null)
            GUI.DrawTexture(new Rect(10,10,256,256),target,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if (commands != null) commands.Release();
        if (target != null) { target.Release(); Destroy(target); }
        if (material != null) Destroy(material);
        if (mesh != null) Destroy(mesh);
    }
}
