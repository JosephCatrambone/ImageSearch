package com.josephcatrambone.imagesearch.Search;

import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.RequestMapping;
import static org.springframework.web.bind.annotation.RequestMethod.POST;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SpiderController {
	private final AtomicLong counter = new AtomicLong();

	@RequestMapping(value="/report", method=POST)
	public String submitFinding(
			@RequestParam(value="image", required=true, defaultValue="") String image, 
			@RequestParam(value="searchMethod", required=false, defaultValue="") String searchMethod
		) {
		return "thx";
	}
}