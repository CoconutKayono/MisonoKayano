Shader "Encyclopedia/B08StencilLab"
{
    Properties
    {
        [IntRange] _Ref("Writer Ref",Range(0,255))=8
        [IntRange] _ReadMask("Writer ReadMask",Range(0,255))=8
        [IntRange] _WriteMask("Writer WriteMask",Range(0,255))=8
        [Enum(UnityEngine.Rendering.CompareFunction)] _Comp("Writer Comp",Float)=8
        [Enum(UnityEngine.Rendering.CompareFunction)] _MaskZTest("Writer ZTest",Float)=8
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        HLSLINCLUDE
        float4 VertMask(float3 p:POSITION):SV_POSITION { return float4(p.xy*0.5,0.5,1); }
        float4 VertFull(float3 p:POSITION):SV_POSITION { return float4(p.xy,0.5,1); }
        float4 FragMask():SV_Target { return 0; }
        float4 FragColor():SV_Target { return float4(0,0.5,1,1); }
        ENDHLSL
        Pass
        {
            Name "Writer"
            Cull Off
            ZWrite Off
            ZTest [_MaskZTest]
            ColorMask 0
            Stencil
            {
                Ref [_Ref]
                ReadMask [_ReadMask]
                WriteMask [_WriteMask]
                Comp [_Comp]
                Pass Replace
                Fail Zero
                ZFail Invert
            }
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex VertMask
            #pragma fragment FragMask
            ENDHLSL
        }
        Pass
        {
            Name "Reader"
            Cull Off
            ZWrite Off
            ZTest Always
            Blend Off
            Stencil
            {
                Ref 8
                ReadMask 8
                WriteMask 0
                Comp Equal
                Pass Keep
                Fail Keep
                ZFail Keep
            }
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex VertFull
            #pragma fragment FragColor
            ENDHLSL
        }
    }
}
