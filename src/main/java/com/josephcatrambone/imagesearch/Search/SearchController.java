package com.josephcatrambone.imagesearch.Search;

import java.util.concurrent.atomic.AtomicLong;
import org.springframework.web.bind.annotation.RequestMapping;
import static org.springframework.web.bind.annotation.RequestMethod.*;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchController {
	private final AtomicLong counter = new AtomicLong();

	@RequestMapping(value="/search", method=POST)
	public Query submitQuery(
			@RequestParam(value="image", required=true, defaultValue="") String image, 
			@RequestParam(value="searchMethod", required=false, defaultValue="") String searchMethod
		) {
		return new Query(counter.incrementAndGet(), null);
	}
	
	/*** getQueryResults
	 * Get the latest results for the specified query ID.
	 * @param id The unique ID of the query returned from submitQuery.
	 * @param page The page of results.
	 * @return 
	 */
	@RequestMapping(value="/search", method=GET)
	public ResultSet getQueryResults(
			@RequestParam(value="id", required=true, defaultValue="") String id, 
			@RequestParam(value="page", required=false, defaultValue="0") String page
		) {
		return new ResultSet(Long.parseLong(id), Integer.parseInt(page), null);
	}
}

/** Alternative
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@RequestMapping("/hello-world")
public class HelloWorldController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @RequestMapping(method=RequestMethod.GET)
    public @ResponseBody Greeting sayHello(@RequestParam(value="name", required=false, defaultValue="Stranger") String name) {
        return new Greeting(counter.incrementAndGet(), String.format(template, name));
    }

}
*/
