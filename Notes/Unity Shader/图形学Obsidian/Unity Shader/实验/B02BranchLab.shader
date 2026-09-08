Shader "Encyclopedia/B02BranchLab"
{
    Properties
    {
        [Enum(AllA,0,AllB,1,LargeTiles,2,PixelChecker,3)] _Mode("Branch Pattern", Float)=0
        _TilePixels("Large Tile Size", Range(8,256))=64
        _Seed("Runtime Seed", Range(0.01,1))=0.3
    }
    SubShader
    {
        Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" }
        Pass
        {
            Tags { "LightMode"="UniversalForward" }
            HLSLPROGRAM
            #pragma target 3.5
            #pragma vertex Vert
            #pragma fragment Frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
            CBUFFER_START(UnityPerMaterial)
                float _Mode;
                float _TilePixels;
                float _Seed;
            CBUFFER_END
            struct A { float4 p:POSITION; float2 uv:TEXCOORD0; };
            struct V { float4 p:SV_POSITION; float2 uv:TEXCOORD0; };
            V Vert(A input)
            {
                V output;
                output.p=TransformObjectToHClip(input.p.xyz);
                output.uv=input.uv;
                return output;
            }
            float WorkA(float x)
            {
                [loop] for(int k=0;k<24;k++) x=frac(x*1.31+0.17);
                return x;
            }
            float WorkB(float x)
            {
                [loop] for(int k=0;k<24;k++) x=frac(x*1.73+0.29);
                return x;
            }
            half4 Frag(V input):SV_Target
            {
                bool chooseA;
                if(_Mode<0.5) chooseA=true;
                else if(_Mode<1.5) chooseA=false;
                else
                {
                    float tile=_Mode<2.5 ? max(_TilePixels,1.0) : 1.0;
                    float2 cell=floor(input.p.xy/tile);
                    chooseA=fmod(cell.x+cell.y,2.0)<1.0;
                }
                float value;
                [branch] if(chooseA) value=WorkA(input.uv.x+_Seed);
                else value=WorkB(input.uv.x+_Seed);
                return half4(value,value,value,1);
            }
            ENDHLSL
        }
    }
}
