package com.josephcatrambone.imagesearch.Search;

/**
 *
 * @author jcatrambone
 */
public class ResultSet {
	private long id;
	private final long queryId;
	private int page;
	private String[] results;
	
	public ResultSet(long queryId, int page, String[] results) {
		this.queryId = queryId;
		this.page = page;
		this.results = results;
	}
}
