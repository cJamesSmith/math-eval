CUDA_VISIBLE_DEVICES='0,1,2,3' \
VLLM_WORKER_MULTIPROC_METHOD=spawn \
python eval.py \
--model_name_or_path "Qwen/Qwen2.5-7B" \
--data_name "aime" \
--prompt_type "qwen-instruct" \
--temperature 0.6 \
--start_idx 0 \
--end_idx -1 \
--n_sampling 1024 \
--k 256 \
--split "test" \
--max_tokens 16384 \
--seed 0 \
--top_p 0.95 \
--surround_with_messages \

