package com.josephcatrambone.imagesearch.Search;
import java.awt.image.BufferedImage;

/**
 *
 * @author jcatrambone
 */
public class ImageReference {
	private final long id; // Primary key.
	private final long imageId; // Foreign key.
	private final String url; // URL of the image
	private final String thumbnail; // Base64 thumbnail of the image.
	private final String metadata; // JSON array of image metadata.
	
	public ImageReference(long id, long imageReference, String url, String thumbnail, String metadata) {
		this.id = id;
		this.imageId = imageReference;
		this.url = url;
		this.thumbnail = thumbnail;
		this.metadata = metadata;
	}
	
	public long getId() {
		return id;
	}
	
	public String getUrl() {
		return url;
	}
	
	/***
	 * @return The long ID of the image which this references.  NOT the ID of the source.
	 */
	public long getImageId() {
		return imageId;
	}
	
	public String getThumbnailBase64() {
		return thumbnail;
	}
	
	public BufferedImage getThumbnail() {
		return null;
	}
	
	public String getMetadata() {
		return metadata;
	}
	
	public Object getMetadata(String field) {
		return null;
	}
}
