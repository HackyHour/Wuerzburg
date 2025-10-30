// Vertex shader

struct VertexInput {
    @location(0) position: vec3<f32>,
    @location(1) color: vec3<f32>,
};

struct VertexOutput {
    @builtin(position) clip_position: vec4<f32>,
};

@vertex
fn vs_main(
    model: VertexInput,
) -> VertexOutput {
    var out: VertexOutput;
    out.clip_position = vec4<f32>(model.position, 1.0);
    return out;
}

// Fragment shader

fn color_map(coord: vec2<f32>,) -> vec4<f32> {
    var color: vec4<f32>;
    color = vec4<f32>(0.0,0.0, 0.0, 1.0);
    
    var u: vec2<f32>;
    var z: vec2<f32>;

    let max_iter = 1000;
    var iter: i32;

    var x_t: f32;

    iter = 0;
    z = vec2<f32>(0.0,0.0);

    u.x = (coord.x - 640.0)/400.0;
    u.y = -1.0*(coord.y - 400.0)/400.0;
    while iter < max_iter {
        x_t = z.x*z.x - z.y*z.y + u.x;
        z.y = 2.0*z.x*z.y + u.y;
        z.x = x_t;
        if z.x*z.x + z.y*z.y > 2.0*2.0 {
            
            color.x = sin(-9.0* log(f32(iter)/f32(max_iter))/(1.0 - log(f32(iter)/f32(max_iter))));
            color.y = cos(-9.0* log(f32(iter)/f32(max_iter))/(1.0 - log(f32(iter)/f32(max_iter))));
            //if iter < 20 {
            //    color.x = 1.0 - f32(iter)/f32(max_iter);
            //} else {
            //    color.y = 1.0 - f32(iter)/f32(max_iter);
            //}
            break;
        }
        iter = iter + 1;
    }

    return color;

}

@fragment
fn fs_main(in: VertexOutput) -> @location(0) vec4<f32> {
    return color_map(in.clip_position.xy);
}
