Shader "Encyclopedia/D01ListLab"
{
    Properties { _Color("Base Color",Color)=(0.2,0.6,1,1) }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        CBUFFER_START(UnityPerMaterial)
            float4 _Color;
        CBUFFER_END
        float4 Vert(float3 p:POSITION):SV_POSITION { return TransformObjectToHClip(p); }
        float4 BaseFrag():SV_Target { return _Color; }
        float4 MaskFrag():SV_Target { return float4(1,0,1,1); }
        ENDHLSL
        Pass
        {
            Name "BaseColor"
            Tags { "LightMode"="SRPDefaultUnlit" }
            ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment BaseFrag
            ENDHLSL
        }
        Pass
        {
            Name "MaskPass"
            Tags { "LightMode"="D01Mask" }
            ZWrite Off ZTest LEqual
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment MaskFrag
            ENDHLSL
        }
    }
}
