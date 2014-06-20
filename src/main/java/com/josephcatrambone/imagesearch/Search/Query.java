package com.josephcatrambone.imagesearch.Search;

public class Query {
	private final long id;
	private final String target;
	//private final byte[][] ingroup;
	//private final byte[][] outgroup;
	
	public Query(long id, String target) {
		this.id = id;
		this.target = target;
	}
	
}
