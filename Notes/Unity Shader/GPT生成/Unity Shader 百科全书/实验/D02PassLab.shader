Shader "Encyclopedia/D02PassLab"
{
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        float4 Vert(float3 p:POSITION):SV_POSITION { return TransformObjectToHClip(p); }
        float4 BaseFrag():SV_Target { return float4(0.15,0.4,1,1); }
        float4 InspectFrag():SV_Target { return float4(1,1,0,1); }
        ENDHLSL
        Pass
        {
            Name "VisibleBase"
            Tags { "LightMode"="SRPDefaultUnlit" }
            ZWrite On ZTest LEqual
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment BaseFrag
            ENDHLSL
        }
        Pass
        {
            Name "NamedInspectPass"
            Tags { "LightMode"="D02Inspect" }
            ZWrite Off ZTest Never
            HLSLPROGRAM
            #pragma vertex Vert
            #pragma fragment InspectFrag
            ENDHLSL
        }
    }
}
