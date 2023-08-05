//this file is autogenerated using stringify.bat (premake --stringify) in the build folder of this project
static const char* linesVertexShader =
	"#version 150   \n"
	"uniform mat4 ModelViewMatrix;\n"
	"uniform mat4 ProjectionMatrix;\n"
	"uniform vec4 colour;\n"
	"in vec4 position;\n"
	"out vec4 colourV;\n"
	"void main (void)\n"
	"{\n"
	"    colourV = colour;\n"
	"		gl_Position = ProjectionMatrix * ModelViewMatrix * position;\n"
	"		\n"
	"}\n";
