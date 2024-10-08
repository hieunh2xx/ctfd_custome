using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace kctf_service.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class KCTFController : ControllerBase
    {
        [HttpGet]
        public IActionResult GetAllCluster()
        {
            return Ok();
        }
    }


}
