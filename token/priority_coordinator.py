"""
Token-Integrated Workflow Coordinator
Priority job scheduling based on token staking
"""
import time
import heapq
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class PriorityQueue:
    """Priority queue for job scheduling based on stake priority."""
    
    def __init__(self):
        self.queue = []
        self.counter = 0
    
    def add_job(self, priority: float, job: Dict[str, Any]):
        """Add job to queue with priority (higher = more important)."""
        # Use negative priority for max-heap behavior
        heapq.heappush(self.queue, (-priority, self.counter, job))
        self.counter += 1
    
    def get_next_job(self) -> Optional[Dict[str, Any]]:
        """Get highest priority job."""
        if self.queue:
            _, _, job = heapq.heappop(self.queue)
            return job
        return None
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.queue) == 0
    
    def size(self) -> int:
        """Get queue size."""
        return len(self.queue)


class TokenIntegratedCoordinator:
    """
    Enhanced workflow coordinator with token integration.
    Manages priority scheduling and token-gated features.
    """
    
    def __init__(
        self, 
        base_coordinator, 
        token_manager,
        staking_system,
        access_control
    ):
        """
        Initialize token-integrated coordinator.
        
        Args:
            base_coordinator: Original WorkflowCoordinator
            token_manager: TokenManager instance
            staking_system: StakingSystem instance
            access_control: AccessControl instance
        """
        self.base_coordinator = base_coordinator
        self.token_manager = token_manager
        self.staking_system = staking_system
        self.access_control = access_control
        
        self.job_queue = PriorityQueue()
        self.active_jobs = {}
        self.completed_jobs = []
        self.job_history = []
    
    def submit_production(
        self, 
        user_id: str, 
        production_request: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit a production request with token validation.
        
        Args:
            user_id: User's ID
            production_request: Production parameters
            
        Returns:
            Job submission result
        """
        print(f"\n{'='*60}")
        print(f"🎬 ANIMA PRODUCTION SUBMISSION")
        print(f"{'='*60}")
        print(f"User: {user_id}")
        print(f"Tier: {self.staking_system.get_user_tier(user_id).value}")
        
        # Validate access
        print("\n🔐 Validating access permissions...")
        validation = self.access_control.validate_production_request(user_id, production_request)
        
        if not validation["valid"]:
            print("\n❌ ACCESS DENIED")
            for violation in validation["violations"]:
                print(f"   • {violation}")
            
            if validation["recommendations"]:
                print("\n💡 Recommendations:")
                for rec in validation["recommendations"]:
                    print(f"   • Stake {rec['additional_stake_needed']:.2f} more ANM to unlock {rec['tier']} tier")
            
            return {
                "success": False,
                "error": "Access validation failed",
                "validation": validation
            }
        
        print("✓ Access validated")
        
        # Calculate cost
        print("\n💰 Calculating production cost...")
        cost = self.access_control.calculate_usage_cost(production_request)
        print(f"   Base cost: {cost:.2f} ANM")
        
        # Check and charge tokens
        print("\n💳 Processing payment...")
        payment_result = self.token_manager.charge_usage_fee(user_id, cost)
        
        if not payment_result["success"]:
            print(f"\n❌ PAYMENT FAILED: {payment_result['error']}")
            return {
                "success": False,
                "error": "Insufficient balance",
                "payment_result": payment_result
            }
        
        print(f"✓ Payment processed: {payment_result['transaction']['total_charged']:.2f} ANM")
        print(f"   Burned: {payment_result['deflationary_impact']['burned']:.2f} ANM")
        print(f"   Reinvested: {payment_result['deflationary_impact']['reinvested']:.2f} ANM")
        print(f"   New balance: {payment_result['new_balance']:.2f} ANM")
        
        # Calculate priority score
        priority_score = self.staking_system.get_priority_score(user_id)
        print(f"\n⚡ Priority score: {priority_score:.2f}")
        
        # Create job
        job_id = f"JOB-{len(self.job_history) + 1:06d}"
        job = {
            "job_id": job_id,
            "user_id": user_id,
            "production_request": production_request,
            "priority_score": priority_score,
            "cost": cost,
            "submitted_at": datetime.now().isoformat(),
            "status": "queued"
        }
        
        # Add to priority queue
        self.job_queue.add_job(priority_score, job)
        self.job_history.append(job)
        
        queue_position = self._get_queue_position(job_id)
        
        print(f"\n✅ JOB SUBMITTED: {job_id}")
        print(f"   Queue position: #{queue_position}")
        print(f"   Priority: {'High' if priority_score > 5 else 'Normal' if priority_score > 2 else 'Standard'}")
        print(f"{'='*60}\n")
        
        return {
            "success": True,
            "job_id": job_id,
            "queue_position": queue_position,
            "priority_score": priority_score,
            "cost": payment_result["transaction"]["total_charged"],
            "estimated_completion": self._estimate_completion_time(queue_position)
        }
    
    def process_next_job(self) -> Optional[Dict[str, Any]]:
        """
        Process the next highest-priority job from the queue.
        
        Returns:
            Production result or None if queue is empty
        """
        job = self.job_queue.get_next_job()
        
        if not job:
            return None
        
        job_id = job["job_id"]
        user_id = job["user_id"]
        production_request = job["production_request"]
        
        print(f"\n{'='*60}")
        print(f"🎬 PROCESSING JOB: {job_id}")
        print(f"   User: {user_id}")
        print(f"   Priority: {job['priority_score']:.2f}")
        print(f"{'='*60}\n")
        
        # Mark as active
        job["status"] = "processing"
        job["started_at"] = datetime.now().isoformat()
        self.active_jobs[job_id] = job
        
        # Execute production using base coordinator
        start_time = time.time()
        production_result = self.base_coordinator.execute_production(production_request)
        processing_time = time.time() - start_time
        
        # Update job
        job["status"] = "completed" if production_result.get("status") == "completed" else "failed"
        job["completed_at"] = datetime.now().isoformat()
        job["processing_time"] = processing_time
        job["production_result"] = production_result
        
        # Move to completed
        del self.active_jobs[job_id]
        self.completed_jobs.append(job)
        
        # Award bonus rewards for completed jobs (optional)
        if job["status"] == "completed":
            self._award_completion_bonus(user_id, job)
        
        return job
    
    def _award_completion_bonus(self, user_id: str, job: Dict[str, Any]):
        """Award small bonus for successful production completion."""
        # Award 0.1% of cost as completion bonus
        bonus = job["cost"] * 0.001
        
        if bonus > 0:
            self.token_manager.mint_tokens(
                user_id, 
                bonus, 
                f"completion_bonus_{job['job_id']}"
            )
    
    def _get_queue_position(self, job_id: str) -> int:
        """Get position of job in queue."""
        # Count jobs with higher or equal priority
        position = 1
        for _, _, queued_job in self.job_queue.queue:
            if queued_job["job_id"] == job_id:
                break
            position += 1
        return position
    
    def _estimate_completion_time(self, queue_position: int) -> str:
        """Estimate completion time based on queue position."""
        # Assume average 2 minutes per job
        minutes = queue_position * 2
        
        if minutes < 60:
            return f"~{minutes} minutes"
        else:
            hours = minutes // 60
            remaining_mins = minutes % 60
            return f"~{hours}h {remaining_mins}m"
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get status of a specific job."""
        # Check active jobs
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            return {
                "job_id": job_id,
                "status": "processing",
                "submitted_at": job["submitted_at"],
                "started_at": job.get("started_at"),
                "elapsed_time": (datetime.now() - datetime.fromisoformat(job["started_at"])).total_seconds()
            }
        
        # Check completed jobs
        for job in self.completed_jobs:
            if job["job_id"] == job_id:
                return {
                    "job_id": job_id,
                    "status": job["status"],
                    "submitted_at": job["submitted_at"],
                    "started_at": job.get("started_at"),
                    "completed_at": job.get("completed_at"),
                    "processing_time": job.get("processing_time")
                }
        
        # Check queue
        for _, _, job in self.job_queue.queue:
            if job["job_id"] == job_id:
                return {
                    "job_id": job_id,
                    "status": "queued",
                    "queue_position": self._get_queue_position(job_id),
                    "submitted_at": job["submitted_at"],
                    "estimated_completion": self._estimate_completion_time(self._get_queue_position(job_id))
                }
        
        return {"error": "Job not found"}
    
    def get_user_jobs(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all jobs for a user."""
        user_jobs = [
            job for job in self.job_history
            if job["user_id"] == user_id
        ]
        return user_jobs
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        return {
            "queued_jobs": self.job_queue.size(),
            "active_jobs": len(self.active_jobs),
            "completed_jobs": len(self.completed_jobs),
            "total_jobs_processed": len(self.job_history)
        }
