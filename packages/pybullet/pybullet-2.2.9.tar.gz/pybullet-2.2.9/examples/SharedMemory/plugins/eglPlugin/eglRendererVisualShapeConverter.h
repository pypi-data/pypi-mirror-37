#ifndef EGL_RENDERER_VISUAL_SHAPE_CONVERTER_H
#define EGL_RENDERER_VISUAL_SHAPE_CONVERTER_H

#include "../../../Importers/ImportURDFDemo/UrdfRenderingInterface.h"

struct EGLRendererVisualShapeConverter : public UrdfRenderingInterface
{
	struct EGLRendererVisualShapeConverterInternalData* m_data;

	EGLRendererVisualShapeConverter();

	virtual ~EGLRendererVisualShapeConverter();

	virtual void convertVisualShapes(int linkIndex, const char* pathPrefix, const btTransform& localInertiaFrame, const UrdfLink* linkPtr, const UrdfModel* model, int shapeUid, int objectIndex);

	virtual int getNumVisualShapes(int bodyUniqueId);

	virtual int getVisualShapesData(int bodyUniqueId, int shapeIndex, struct b3VisualShapeData* shapeData);

	virtual void changeRGBAColor(int bodyUniqueId, int linkIndex, int shapeIndex, const double rgbaColor[4]);

	virtual void changeShapeTexture(int objectUniqueId, int linkIndex, int shapeIndex, int textureUniqueId);

	virtual void removeVisualShape(int shapeUid);

	virtual void setUpAxis(int axis);

	virtual void resetCamera(float camDist, float yaw, float pitch, float camPosX, float camPosY, float camPosZ);

	virtual void clearBuffers(struct TGAColor& clearColor);

	virtual void resetAll();

	virtual void getWidthAndHeight(int& width, int& height);
	virtual void setWidthAndHeight(int width, int height);
	virtual void setLightDirection(float x, float y, float z);
	virtual void setLightColor(float x, float y, float z);
	virtual void setLightDistance(float dist);
	virtual void setLightAmbientCoeff(float ambientCoeff);
	virtual void setLightDiffuseCoeff(float diffuseCoeff);
	virtual void setLightSpecularCoeff(float specularCoeff);
	virtual void setShadow(bool hasShadow);
	virtual void setFlags(int flags);

	virtual void copyCameraImageData(unsigned char* pixelsRGBA, int rgbaBufferSizeInPixels, float* depthBuffer, int depthBufferSizeInPixels, int* segmentationMaskBuffer, int segmentationMaskSizeInPixels, int startPixelIndex, int* widthPtr, int* heightPtr, int* numPixelsCopied);
	void copyCameraImageDataGL(unsigned char* pixelsRGBA, int rgbaBufferSizeInPixels, float* depthBuffer, int depthBufferSizeInPixels, int* segmentationMaskBuffer, int segmentationMaskSizeInPixels, int startPixelIndex, int* widthPtr, int* heightPtr, int* numPixelsCopied);

	virtual void render();
	virtual void render(const float viewMat[16], const float projMat[16]);

	virtual int loadTextureFile(const char* filename);
	virtual int registerTexture(unsigned char* texels, int width, int height);

	virtual void setProjectiveTextureMatrices(const float viewMatrix[16], const float projectionMatrix[16]);
	virtual void setProjectiveTexture(bool useProjectiveTexture);

	virtual void syncTransform(int shapeUid, const class btTransform& worldTransform, const class btVector3& localScaling);
};

#endif  //EGL_RENDERER_VISUAL_SHAPE_CONVERTER_H
