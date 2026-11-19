Shader "Learning/URPDepthExplorer"
{
    Properties
    {
        [Enum(Raw,0,Linear01,1,EyeRange,2)] _View("View", Float) = 2
        _DisplayDistance("Display Distance", Float) = 20
    }

    SubShader
    {
        Tags { "RenderPipeline" = "UniversalPipeline" }

        Pass
        {
            Name "DepthExplorer"
            ZWrite Off
            ZTest Always
            Cull Off
            Blend Off

            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment DepthFragment

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            #include "Packages/com.unity.render-pipelines.core/Runtime/Utilities/Blit.hlsl"
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/DeclareDepthTexture.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float _View;
                float _DisplayDistance;
            CBUFFER_END

            half4 DepthFragment(Varyings input) : SV_Target
            {
                UNITY_SETUP_STEREO_EYE_INDEX_POST_VERTEX(input);

                float2 screenUV = input.texcoord;
                float rawDepth = SampleSceneDepth(screenUV);

                // A small threshold treats the cleared far depth as background.
                // Geometry extremely close to the far plane can also be masked.
                #if UNITY_REVERSED_Z
                    if (rawDepth <= 0.000001)
                        return half4(0.0, 0.0, 0.0, 1.0);
                #else
                    if (rawDepth >= 0.999999)
                        return half4(0.0, 0.0, 0.0, 1.0);
                #endif

                if (_View < 0.5)
                    return half4(rawDepth, rawDepth, rawDepth, 1.0);

                float eyeDepth;
                if (unity_OrthoParams.w > 0.5)
                    eyeDepth = LinearDepthToEyeDepth(rawDepth);
                else
                    eyeDepth = LinearEyeDepth(rawDepth, _ZBufferParams);

                // E / far matches Linear01Depth for standard perspective cameras.
                // Using the converted E also supports ordinary orthographic cameras.
                float gray;
                if (_View < 1.5)
                    gray = eyeDepth / _ProjectionParams.z;
                else
                    gray = eyeDepth / max(_DisplayDistance, 0.0001);

                gray = saturate(gray);
                return half4(gray, gray, gray, 1.0);
            }
            ENDHLSL
        }
    }
    Fallback Off
}
