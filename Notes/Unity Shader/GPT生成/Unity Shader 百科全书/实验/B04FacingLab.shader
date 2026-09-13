Shader "Encyclopedia/B04FacingLab"
{
    Properties
    {
        [Enum(UnityEngine.Rendering.CullMode)] _Cull("Cull", Float)=0
        [Toggle] _ShowNormals("Show Input Normals", Float)=0
        [Toggle] _MirrorX("Mirror Clip X", Float)=0
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            Cull [_Cull]
            ZTest Always
            ZWrite Off
            HLSLPROGRAM
            #pragma target 3.0
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Cull;
                float _ShowNormals;
                float _MirrorX;
            CBUFFER_END
            struct A { float3 p:POSITION; float3 n:NORMAL; };
            struct V { float4 p:SV_POSITION; float3 n:TEXCOORD0; };
            V Vert(A input)
            {
                V output;
                float x=_MirrorX>0.5 ? -input.p.x : input.p.x;
                output.p=float4(x,input.p.y,0.5,1);
                output.n=input.n;
                return output;
            }
            half4 Frag(V input, FRONT_FACE_TYPE facing:FRONT_FACE_SEMANTIC):SV_Target
            {
                float3 faceColor=IS_FRONT_VFACE(facing,float3(0,1,0),float3(1,0,0));
                float3 normalColor=input.n*0.5+0.5;
                return half4(_ShowNormals>0.5 ? normalColor : faceColor,1);
            }
            ENDHLSL
        }
    }
}
