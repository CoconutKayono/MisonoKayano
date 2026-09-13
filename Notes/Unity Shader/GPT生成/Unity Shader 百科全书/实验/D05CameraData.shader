Shader "Encyclopedia/D05CameraData"
{
    Properties
    {
        _DepthRange("Depth Display Range (meters)", Float) = 20
        _MotionScale("Motion Display Gain", Float) = 20
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" }
        Cull Off ZWrite Off ZTest Always
        HLSLINCLUDE
        #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
        #include "Packages/com.unity.render-pipelines.core/ShaderLibrary/Packing.hlsl"
        #define USE_FULL_PRECISION_BLIT_TEXTURE
        #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
        CBUFFER_START(UnityPerMaterial)
            float _DepthRange;
            float _MotionScale;
        CBUFFER_END
        float4 ReadData(Varyings i)
        {
            return SAMPLE_TEXTURE2D_X(_BlitTexture, sampler_PointClamp, i.texcoord);
        }
        float4 ShowDepth(Varyings i) : SV_Target
        {
            float eye = LinearEyeDepth(ReadData(i).r, _ZBufferParams);
            float v = saturate(eye / max(_DepthRange, 0.001));
            return float4(v, v, v, 1);
        }
        float4 ShowNormal(Varyings i) : SV_Target
        {
            float3 n = ReadData(i).xyz;
            #if defined(_GBUFFER_NORMALS_OCT)
                float2 oct = Unpack888ToFloat2(n) * 2.0 - 1.0;
                n = UnpackNormalOctQuadEncode(oct);
            #endif
            return float4(n * 0.5 + 0.5, 1);
        }
        float4 ShowMotion(Varyings i) : SV_Target
        {
            float2 v = 0.5 + ReadData(i).rg * _MotionScale;
            return float4(saturate(v), 0.5, 1);
        }
        ENDHLSL
        Pass
        {
            Name "DepthDisplay"
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment ShowDepth
            ENDHLSL
        }
        Pass
        {
            Name "NormalDisplay"
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment ShowNormal
            #pragma multi_compile_fragment _ _GBUFFER_NORMALS_OCT
            ENDHLSL
        }
        Pass
        {
            Name "MotionDisplay"
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment ShowMotion
            ENDHLSL
        }
    }
}
