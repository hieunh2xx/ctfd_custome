using System.Diagnostics;
using System.Text;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace kctf_service.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class KCTFController : ControllerBase
    {
        [HttpGet("/getallcluster")]
        public IActionResult GetAllCluster()
        {
            // Create a new process
            Process process = new Process();
            StringBuilder  arguments = new StringBuilder("");
            arguments.Append("cd - && cd ctf-directory && source kctf/activate && kctf cluster list");
            // Set the process start info
            process.StartInfo.FileName = "/bin/bash";
            process.StartInfo.Arguments = $"-c \"{arguments}\"";
            process.StartInfo.RedirectStandardOutput = true; // Capture the output
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.CreateNoWindow = true; // Don't create a terminal window

            // Start the process
            process.Start();

            // Read the output
            string result = process.StandardOutput.ReadToEnd();

            // Wait for the process to exit
            process.WaitForExit();
            return Ok(result);
        }
    }


}
