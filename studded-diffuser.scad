
baseWidth = 14.5+3*2;
baseHeight = 1.0;
baseLength = 62.5;
//$fs = 0.1;
//$fa = 10;

// TEST SEGMENT
baseLength = 20.0;

lensThickness = 1.0;
lensRadius    = baseWidth/2;

clipAboveHeight     = 1.0;
clipRidgeHeight     = 1.0;
clipBelowHeight     = 1.0;
clipInset           = 1.0;
clipHeight = clipAboveHeight+clipRidgeHeight+clipBelowHeight;
squash              = 1.0;

studBase            = 7;
studHeight          = 3; // keep studHeight <= studBase to keep overhangs <= 45%

module clip()
{
    translate([clipHeight/2,lensRadius-lensThickness/2,0])
      cube([clipHeight,lensThickness,baseLength], center=true);
    translate([clipAboveHeight+clipRidgeHeight/2, lensRadius-lensThickness/2-clipInset/2-lensThickness/2,0])
      cube([clipRidgeHeight,clipInset,baseLength], center=true);
    
}

module lens()
{
  scale([squash,1,1])
    difference() {
      cylinder(h=baseLength, r=lensRadius, center=true);
      translate([lensRadius+1,0,0])
        cube([lensRadius*2+1,lensRadius*2+1,baseLength+1], center=true);
      cylinder(h=baseLength+1, r=lensRadius-lensThickness, center=true);
    }
}

module stud_row(count, offset=0)
{
  studRad = studBase * 1.41421356 / 2.0;
  studAngle = 28;
  studAngle0 = -(count-1)/2*studAngle;

  for (i = [0 : count-1]) {
    rotate(a=studAngle0 + studAngle * i, v=[0,0,1])
      rotate(a=90, v=[0,1,0])
        translate([0,0,-studHeight-lensRadius+lensThickness+offset])
	      cylinder(h=studHeight, r1=0, r2=studRad, $fs=0.1, $fa=60);
  }
}

module stud_rows(offset=0)
{
  stud_row(5,offset);
  translate([0,0,4])
    stud_row(6,offset);
  translate([0,0,-4])
    stud_row(6,offset);

}

module stud_positive()
{
  stud_rows(0);
}

module stud_negative()
{
  stud_rows(1);
}

difference() {
  union() {
    lens();
    stud_positive();
  }
  stud_negative();
}

clip();
mirror([0,1,0])clip();

