def triangle_area(a,b,c):
    # Heron's formula
    return abs( (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1]) )

def triangle_point_collision(triangle, p) -> bool:
    a, b, c = triangle
    original_area = triangle_area(a,b,c)
    area1 = triangle_area(p,a,b)
    area2 = triangle_area(p,a,c)
    area3 = triangle_area(p,b,c)
    return area1 + area2 + area3 == original_area

