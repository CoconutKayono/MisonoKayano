using UnityEngine;
using UnityEngine.Rendering;

public class C06DependencyLab : MonoBehaviour
{
    public ComputeShader program;
    public bool consumeBeforeGenerate;
    RenderTexture source, result;
    CommandBuffer commands;
    int generate, consume, step;
    bool ready;

    void Start()
    {
        if(program==null || !SystemInfo.supportsComputeShaders ||
           !SystemInfo.SupportsRandomWriteOnRenderTextureFormat(RenderTextureFormat.ARGBFloat))
        {
            Debug.LogError("C06 requires compute and ARGBFloat random writes.");
            return;
        }
        source=MakeTarget("C06 Source");
        result=MakeTarget("C06 Result");
        if(!source.IsCreated() || !result.IsCreated()) return;
        generate=program.FindKernel("Generate");
        consume=program.FindKernel("Consume");
        commands=new CommandBuffer { name="C06 Produce Consume" };
        commands.SetRenderTarget(source);
        commands.ClearRenderTarget(false,true,Color.black);
        commands.SetRenderTarget(result);
        commands.ClearRenderTarget(false,true,Color.black);
        Graphics.ExecuteCommandBuffer(commands);
        ready=true;
        RunNextStep();
    }
    RenderTexture MakeTarget(string label)
    {
        var t=new RenderTexture(128,128,0,RenderTextureFormat.ARGBFloat,RenderTextureReadWrite.Linear);
        t.name=label;
        t.enableRandomWrite=true;
        t.filterMode=FilterMode.Point;
        if(!t.Create()) Debug.LogError("C06 failed to create "+label);
        return t;
    }
    void RecordGenerate()
    {
        commands.SetComputeIntParam(program,"_Step",step);
        commands.SetComputeTextureParam(program,generate,"_Write",source);
        commands.DispatchCompute(program,generate,16,16,1);
    }
    void RecordConsume()
    {
        commands.SetComputeTextureParam(program,consume,"_Read",source);
        commands.SetComputeTextureParam(program,consume,"_Write",result);
        commands.DispatchCompute(program,consume,16,16,1);
    }
    [ContextMenu("Run Next Step")]
    public void RunNextStep()
    {
        if(!ready) return;
        step++;
        commands.Clear();
        if(consumeBeforeGenerate) { RecordConsume(); RecordGenerate(); }
        else { RecordGenerate(); RecordConsume(); }
        Graphics.ExecuteCommandBuffer(commands);
    }
    void OnGUI()
    {
        if(!ready) return;
        if(GUI.Button(new Rect(10,10,180,30),"Run Next Step")) RunNextStep();
        GUI.Label(new Rect(10,45,650,25),"Step "+step+" | Source (left), Result (right)");
        GUI.DrawTexture(new Rect(10,80,256,256),source,ScaleMode.ScaleToFit,false);
        GUI.DrawTexture(new Rect(280,80,256,256),result,ScaleMode.ScaleToFit,false);
    }
    void OnDestroy()
    {
        if(commands!=null) commands.Release();
        if(source!=null) { source.Release(); Destroy(source); }
        if(result!=null) { result.Release(); Destroy(result); }
    }
}
