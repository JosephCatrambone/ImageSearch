/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.josephcatrambone.imagesearch.Search;

/**
 *
 * @author jcatrambone
 */
public class ImageSource {
	private final long id; // Primary key.
	private final long imageId; // Foreign key.
	private final String url;
	
	public ImageSource(long id, long imageReference, String url) {
		this.id = id;
		this.imageId = imageReference;
		this.url = url;
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
}
